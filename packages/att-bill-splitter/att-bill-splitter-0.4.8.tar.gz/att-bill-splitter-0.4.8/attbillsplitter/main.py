# -*- coding: utf-8 -*-
"""Main module"""

from __future__ import print_function, unicode_literals
import datetime as dt
import re
import click
import peewee as pw
import requests
from bs4 import BeautifulSoup, Tag
from slugify import slugify

# import fake_useragent
from attbillsplitter.errors import ParsingError
from attbillsplitter.models import (
    User, ChargeCategory, ChargeType, BillingCycle, Charge, MonthlyBill, db
)


CHROME_AGENT = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36')
# CHROME_AGENT = fake_useragent.UserAgent().chrome


def create_tables_if_not_exist():
    """Create tables in database if tables do not exist.

    Tables will be created for following models:
        - User
        - ChargeCategory
        - ChargeType
        - BillingCycle
        - Charge
        - MonthlyBill
    """
    db.connect()
    for model in (User, ChargeCategory, ChargeType, BillingCycle, Charge,
                  MonthlyBill):
        if not model.table_exists():
            model.create_table()


def get_start_end_date(bc_name):
    """Get start date and end date for a billing cycle name using regex.

    :param bc_name: name of billing cycle in format of
        'Mar 15 - Apr 14, 2016'
    :type bc_name: str
    :returns: a tuple of start date (datetime.date) and end date
    :rtype: tuple
    """
    m = re.search(r'(\w+ \d+) - (\w+ \d+), (\d{4})', bc_name)
    start_date_str = '{}, {}'.format(m.group(1), m.group(3))
    end_date_str = '{}, {}'.format(m.group(2), m.group(3))
    start_date = dt.datetime.strptime(start_date_str, '%b %d, %Y').date()
    end_date = dt.datetime.strptime(end_date_str, '%b %d, %Y').date()
    return (start_date, end_date)


def aggregate_wireless_monthly(bc):
    """Aggregate wireless charges among all lines.

    :param bc: billing_cycle object
    :type bc: BillingCycle
    :returns: None
    """
    if MonthlyBill.select().where(MonthlyBill.billing_cycle == bc).exists():
        print('\U000026A0  Charges already aggregated for {}'.format(
            bc.name).encode("utf-8"))
        return

    query = (
        User
        .select(User,
                pw.fn.SUM(Charge.amount).alias('total'))
        .join(Charge)
        .join(BillingCycle)
        .switch(Charge)
        .join(ChargeType)
        .join(ChargeCategory)
        .where(BillingCycle.id == bc.id,
               ChargeCategory.category == 'wireless')
        .group_by(User, BillingCycle)
        .naive()
    )
    results = query.execute()
    for user in results:
        MonthlyBill.create(user=user, billing_cycle=bc, total=user.total)


class AttBillSplitter(object):
    """Parse AT&T bill and split wireless charges among users.

    Currently tested on AT&T account with U-verse TV, Internet and Mobile
    Share Value Plan (for wireless).
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        headers = {'User-Agent': CHROME_AGENT}
        self.session.headers.update(headers)

    def login(self):
        """Login to your AT&T online account.

        :returns: status of the login (True or False)
        :rtype: bool
        """
        print('\U000025B6  Login started...'.encode("utf-8"))
        login_url = (
            'https://myattdx05.att.com/commonLogin/igate_wam/multiLogin.do'
        )
        # obtain session cookies needed to login
        self.session.get(login_url)
        # soup = BeautifulSoup(pre_login.text, 'html.parser')
        # hidden_inputs = soup.find_all('input', type='hidden')
        # form = {
        #     x.get('name'): x.get('value')
        #     for x in hidden_inputs if x.get('value') and x.get('name')
        # }

        # this information is in a comment tag and is very difficult to parse
        # hard code this for now
        form = {
            'source': 'MYATT',
            'flow_ind': 'LGN',
            'isSlidLogin': 'true',
            'vhname': 'www.att.com',
            'urlParameters': ('fromdlom=true&reportActionEvent=A_LGN_LOGIN_SUB'
                              '&loginSource=olam'),
            'myATTIntercept': 'false',
            'persist': 'Y',
            'rootPath': '/olam/English'
        }
        form.update({'userid': self.username, 'password': self.password})
        login_submit = self.session.post(login_url, data=form)
        # open('test.html', 'w').write(login_submit.text.encode('utf-8'))
        if 'Manage your account' in login_submit.text:
            print('\U00002705  Login succeeded.'.encode("utf-8"))
            return True
        else:
            if 'promo' in login_submit.url.lower():
                if not self.click_skip_promo():
                    print ('\U0001F534  Popup window detected during login. '
                           'Please login you account in a browser and click '
                           'through. Log out your account before you retry. '
                           '(Sometimes you might have to do this multiple times.'.encode("utf-8"))
                    return False
                return True

            print('\U0001F6AB  Login failed. Please check your username and '
                  'password and retry. Or something unexpected happened.'.encode("utf-8"))
            return False

    def click_skip_promo(self):
        """Request to skip the promo popup

        :returns: status of the skip request (True or False)
        :rtype: bool
        """
        reject_promo_link = (
            'https://www.att.com/olam/rejectPromoUserResponse.myworld'
        )
        skip_promo = self.session.get(reject_promo_link, params={
            'response': 'rejected',
            'reportActionEvent': 'A_LGN_PROMO_DECLINED_SUB'
        })
        return skip_promo.status_code == requests.codes.ok

    def get_history_bills(self):
        """Get history bills.

        :yields: tuple of billing_cycle name and link to the bill
        """
        # this request will add some cookie
        self.session.get(
            'https://www.att.com/olam/passthroughAction.myworld',
            params={'actionType': 'ViewBillHistory'}
        )

        # obtain account number from bill detail page
        # seems like for accounts with uverse services, the link to get the account
        # number is different, so is link to bill.
        # we first try to get account number assuming you have only wireless service
        # if that fails, we will try the uverse option.
        uverse_url = ('https://www.att.com/olam/acctInfoView.myworld?'
                      'actionEvent=displayProfileInformation')
        wireless_url = 'https://www.att.com/olam/ViewBillDetailsAction.myworld'
        an_req = self.session.get(wireless_url)
        act_num_full = re.search(
            'wirelessAccountNumber":"[0-9]+"', an_req.text)
        if act_num_full:
            bill_statement_id_template = '{}|{}|T01|W'
            try:
                act_num_str = act_num_full.group(0)
            except AttributeError as e:
                print(
                    'Something went wrong. Could not find account number from bill detail page.')
                raise ParsingError('Account number not found!')
            act_num = re.search('[0-9]+', act_num_str).group(0)
        else:
            an_req = self.session.get(uverse_url)
            bill_statement_id_template = '{}|{}|T06|V'
            an_soup = BeautifulSoup(an_req.text, 'html.parser')
            act_num_tag = an_soup.find('span', class_='account-number')
            m = re.search(r'.?(\d+).?', act_num_tag.text, re.DOTALL)
            if not m:
                print(
                    'Something went wrong. Could not find account number from bill detail page.')
                raise ParsingError('Account number not found!')
            act_num = m.group(1)

        # now we can get billing history
        bh_req = self.session.get(
            'https://www.att.com/olam/billingPaymentHistoryAction.myworld',
            params={'action': 'ViewBillHistory'}
        )
        bh_req.raise_for_status()
        bh_soup = BeautifulSoup(bh_req.text, 'html.parser')
        bc_tags = bh_soup.find_all('td', headers=['bill_period'])
        for tag in bc_tags:
            bc_name = tag.contents[0]
            end_date_name = bc_name.split(' - ')[1]
            end_date = dt.datetime.strptime(end_date_name, '%b %d, %Y')
            end_date_str = end_date.strftime('%Y%m%d')
            bill_statement_id = bill_statement_id_template.format(
                end_date_str, act_num)
            yield (bc_name, bill_statement_id)

    def parse_user_info(self, bill_html):
        """Parse the bill to find name and number for each line and create
        users. Account holder should be the first entry.

        :returns: list of user objects
        :rtype: list
        :returns: None
        """
        users = []
        soup = BeautifulSoup(bill_html, 'html.parser')
        number_tags = soup.find_all('div', string=re.compile('Total for'))
        for num_tag in number_tags:
            number = num_tag.text.lstrip('Total for')
            # get name for number
            name_tag = soup.find('div', class_='accRow bold MarTop10',
                                 string=re.compile('{}'.format(number)))
            name = name_tag.text.rstrip(' {}'.format(number))
            user, _ = User.get_or_create(name=name, number=number)
            users.append(user)
        return users

    def split_bill(self, bc_name, bill_statement_id):
        """Parse bill and split wireless charges among users.

        Currently not parsing U-Verse charges.
        :param bc_name: billing cycle name
        :type bc_name: str
        :param bill_statement_id: bill statement id, used in link
        :type bill_statement_id: str
        :returns: None
        """
        bill_link_template = (
            'https://www.att.com/olam/billPrintPreview.myworld?'
            'fromPage=history&billStatementID={}'
        )
        bill_req = self.session.get(
            bill_link_template.format(bill_statement_id))
        bill_html = bill_req.text
        if 'Account Details' not in bill_html:
            raise ParsingError('Failed to retrieve billing page')

        soup = BeautifulSoup(bill_html, 'html.parser')
        start_date, end_date = get_start_end_date(bc_name)
        billing_cycle = BillingCycle.create(name=bc_name,
                                            start_date=start_date,
                                            end_date=end_date)

        # parse user name and number
        users = self.parse_user_info(bill_html)
        if not users:
            return

        account_holder_name = soup.find(
            'span', class_='hidden-spoken ng-binding').parent.next_sibling.next_sibling.text.strip()
        account_holder = [
            user for user in users if user.name == account_holder_name][0]
        # --------------------------------------------------------------------
        # Wireless
        # --------------------------------------------------------------------
        wireless_charge_category, _ = ChargeCategory.get_or_create(
            category='wireless',
            text='Wireless'
        )
        charged_users = [account_holder]
        name, number = account_holder.name, account_holder.number
        offset = 0.0
        # charge section starts with user name followed by his/her number
        target = soup.find('div',
                           string=re.compile('{} {}'.format(name, number)))
        # fetch data usage in case there is an overage
        usage_req = self.session.post(
            'https://www.att.com/olam/billUsageTiles.myworld',
            data={'billStatementID': bill_statement_id}
        )
        usage_soup = BeautifulSoup(usage_req.text, 'html.parser')
        usages = {}
        overage_charge_type_name = 'data-text-usage-charges'
        overage_charge_type_text = 'Data & Text Usage Charges'
        data_overused = False
        for tag in target.parent.next_siblings:
            # all charge data are in divs
            if not isinstance(tag, Tag) or tag.name != 'div':
                continue

            # charge section ends with Total for number
            if 'Total for {}'.format(number) in tag.text:
                break

            # each charge type has 'accSummary' as one of its css classes
            if 'accSummary' in tag.get('class', []):
                charge_type_text = tag.find('div').text.strip('\n\t')
                if charge_type_text.startswith('Monthly Charges'):
                    charge_type_text = 'Monthly Charges'
                    # account monthly fee will be shared by all users
                    w_act_m = float(
                        re.search(r'\$([0-9.]+)', tag.text).group(1)
                    )
                    # national discount is applied to account monthly fee
                    m = re.search(
                        r'National Account Discount.*?\$([0-9.]+)',
                        tag.text, re.DOTALL
                    )
                    w_act_m_disc = float(m.group(1)) if m else 0.0
                    # this non-zero offset will be used to adjust account
                    # holder's total monthly charge
                    offset = w_act_m - w_act_m_disc

                m = re.search(
                    r'Total {}.*?\$([0-9.]+)'.format(charge_type_text),
                    tag.text,
                    flags=re.DOTALL
                )
                charge_type_name = slugify(charge_type_text)

                # check if it's a data overage which needs to be shared proportionaly
                if charge_type_name == overage_charge_type_name:
                    data_overused = True
                    total_overage_charge = float(m.group(1))
                    user_tag = usage_soup.find(
                        'p', string=re.compile(account_holder.name))
                    usage_tag = list(
                        user_tag.parent.parent.parent.next_siblings)[1]
                    usage = float(usage_tag.findChild('strong').text)
                    usages[account_holder] = usage
                    total_data_allowance = float(
                        list(usage_tag.findChild(
                            'strong').next_siblings)[-1].split()[0]
                    )
                else:
                    charge_total = float(m.group(1)) - offset
                    # save data to db
                    # ChargeType
                    charge_type, _ = ChargeType.get_or_create(
                        type=charge_type_name,
                        text=charge_type_text,
                        charge_category=wireless_charge_category
                    )
                    # Charge
                    new_charge = Charge(
                        user=account_holder,
                        charge_type=charge_type,
                        billing_cycle=billing_cycle,
                        amount=charge_total
                    )
                    new_charge.save()
                offset = 0.0

        # iterate regular users
        remaining_users = [u for u in users if u.number != number]
        for user in remaining_users:
            charge_total = 0.0
            name, number = user.name, user.number
            # charge section starts with user name followed by his/her number
            target = soup.find('div',
                               string=re.compile('{} {}'.format(name, number)))
            for tag in target.parent.next_siblings:
                # all charge data are in divs
                if not isinstance(tag, Tag) or tag.name != 'div':
                    continue

                # charge section ends with Total for number
                if 'Total for {}'.format(number) in tag.text:
                    break

                # each charge type has 'accSummary' as one of its css classes
                if 'accSummary' in tag.get('class', []):
                    charge_type_text = tag.find('div').text.strip('\n\t')
                    if charge_type_text.startswith('Monthly Charges'):
                        charge_type_text = 'Monthly Charges'

                    m = re.search(
                        r'Total {}.*?\$([0-9.]+)'.format(charge_type_text),
                        tag.text,
                        flags=re.DOTALL
                    )
                    charge_total = float(m.group(1))
                    # save data to db
                    charge_type_name = slugify(charge_type_text)
                    # ChargeType
                    charge_type, _ = ChargeType.get_or_create(
                        type=charge_type_name,
                        text=charge_type_text,
                        charge_category=wireless_charge_category
                    )
                    # Charge
                    new_charge = Charge(
                        user=user,
                        charge_type=charge_type,
                        billing_cycle=billing_cycle,
                        amount=charge_total
                    )
                    new_charge.save()
            if charge_total > 0:
                charged_users.append(user)
            charge_type, _ = ChargeType.get_or_create(
                type='data-text-usage-charges',
                text='Data & Text Usage Charges',
                charge_category=wireless_charge_category
            )
            # data usages
            user_tag = usage_soup.find('p', string=re.compile(user.name))
            if user_tag:
                usage_tag = list(
                    user_tag.parent.parent.parent.next_siblings)[1]
                usage = float(usage_tag.findChild('strong').text)
                usages[user] = usage

        # update share of account monthly charges for each user
        # also calculate total wireless charges (for verification later)
        act_m_share = (w_act_m - w_act_m_disc) / len(charged_users)
        wireless_total = 0
        for user in charged_users:
            # ChargeType
            charge_type, _ = ChargeType.get_or_create(
                type='wireless-acount-monthly-charges-share',
                text='Account Monthly Charges Share',
                charge_category=wireless_charge_category
            )
            # Charge
            new_charge = Charge(
                user=user,
                charge_type=charge_type,
                billing_cycle=billing_cycle,
                amount=act_m_share
            )
            new_charge.save()
            user_total = Charge.select(
                pw.fn.Sum(Charge.amount).alias('total')
            ).join(
                ChargeType,
                on=Charge.charge_type_id == ChargeType.id
            ).where(
                (Charge.user == user),
                Charge.billing_cycle == billing_cycle,
                ChargeType.charge_category == wireless_charge_category
            )
            wireless_total += user_total[0].total

        if data_overused:
            user_share = total_data_allowance / len(charged_users)
            overages = {k: v - user_share for k,
                        v in usages.iteritems() if v > user_share}
            total_overage = sum(overages.values())
            for user, overage in overages.iteritems():
                overage_charge = overage / total_overage * total_overage_charge
                print('User {} over used {} GB data, will be charged extra ${:.2f}'.format(
                    user.name, overage, overage_charge)
                )
                charge_type, _ = ChargeType.get_or_create(
                    type=overage_charge_type_name,
                    text=overage_charge_type_text,
                    charge_category=wireless_charge_category
                )
                # Charge
                new_charge = Charge(
                    user=user,
                    charge_type=charge_type,
                    billing_cycle=billing_cycle,
                    amount=overage_charge
                )
                new_charge.save()
        # aggregate
        aggregate_wireless_monthly(billing_cycle)

    def run(self, lag, force):
        """
        :param lag: a list of lags indicating which bills to split
        :type lag: list
        :param force: a flag to force splitting the bill
        :type force: bool
        :returns: None
        """
        if not self.login():
            return

        for i, (bc_name, bill_statement_id) in enumerate(self.get_history_bills()):
            # if lag is not empty, only split bills specified
            if lag and (i not in lag) and not force:
                continue

            # check if billing cycle already exist
            if BillingCycle.select().where(
                    BillingCycle.name == bc_name
            ):
                print('\U000026A0  Billing Cycle {} already '
                      'processed.'.format(bc_name).encode("utf-8"))
                continue

            print('\U0001F3C3  Start splitting bill {}...'.format(
                bc_name).encode("utf-8"))
            self.split_bill(bc_name, bill_statement_id)
            print('\U0001F3C1  Finished splitting bill {}.'.format(
                bc_name).encode("utf-8"))


@click.command()
@click.option('--lag', '-l', multiple=True, type=int,
              help=('Lag of the bill you want to split with respect to '
                    'current bill. 0 refers to the most recent bill, 1 '
                    'refers to the bill from previous month. Can be used '
                    'multiple times.'))
@click.option('--force', '-f', default=False,
              help=('Force to split the bill (and save) even if the bill has '
                    'already been split before.'))
@click.option('--username', prompt='\U0001F464  AT&T Username',
              help='Username')
@click.option('--password', prompt='\U0001F5DD  AT&T Password',
              hide_input=True, help='Password')
def run_split_bill(username, password, lag, force):
    """Split AT&T wireless bills among lines.

    By default all new (unsplit) bills will be split. If you want to select
    bills to split, use the --lag (-l) option.
    """
    create_tables_if_not_exist()
    splitter = AttBillSplitter(username, password)
    splitter.run(lag, force)
