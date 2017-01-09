# -*- coding: utf-8 -*-

from lxml import html
import requests
from houses.models import *
import logging
from django.db.models import Q

# Get an instance of a logger
logger = logging.getLogger(__name__)


def importAllAgencies(source_name, country_name):
    """
    Will import all real state following the last depth Territorial Entity
    """
    logger.info("START Import all Agencies in " + country_name + ' for ' + source_name + '. This will take a while...')
    Agency.objects.all().delete()
    country = Country.objects.get(country_name=country_name)
    source = Source.objects.get(source_name=source_name)
    # only implemented for Idealista & Spain
    if source.slug == 'id' and country_name == 'Spain':
        sale_transaction = Transaction.objects.get(transaction_name='sale', depth_number=0)
        house_transaction = Transaction.objects.get(transaction_name='house', father=sale_transaction)
        territorial_leaves_list = TerritorialEntity.objects.filter(depth_last=True, country=country)
        for territorial_leaf in territorial_leaves_list:
            url = source.url + "pro/" + SourceTransaction.objects.get(source=source, transaction=sale_transaction).source_transaction_name + source.separator_url + SourceTransaction.objects.get(source=source, transaction=house_transaction).source_transaction_name + '/' + URLSourceTerritory.objects.get(source=source, territory=territorial_leaf).url_source_territory_name_list + "/agencias-inmobiliarias-"
            collectAgencies(source, url, territorial_leaf, 1)
        logger.info("END Import all Agencies in " + country_name + ' for ' + source_name + '.')
    else:
        logger.warning('Only Idealista - Spain is implemented')


def collectAgencies(source, url_base, territorial_leaf, page_number):
    """
    For every page in the territorial_leafe agency page collect and compose the Agencies
    """
    url = url_base + str(page_number)
    try:
        # collect and compose a tree for a url page
        page = requests.get(url)
        tree = html.fromstring(page.content)
        agency_name = tree.xpath('//dl[@class="item"]//span[@class="comm-name"]/text()')
        agency_source_url = tree.xpath('//dl[@class="item"]/dd/a/@href')
        # if all list all same length
        if len(agency_name) == len(agency_source_url) and len(agency_name) != 0:
            list_agencies = zip(agency_name, agency_source_url)
            for agency_item in list_agencies:
                agency = Agency.objects.get_or_create(agency_name=agency_item[0])
                agency_localization = AgencyLocalization.objects.get_or_create(agency=agency[0], place=territorial_leaf)
                agency_localization_source = AgencyLocalizationSource.objects.get_or_create(source=source, agency_localization=agency_localization[0], agency_source_name=agency_item[1].split('/')[2], agency_source_url=agency_item[1])
                # completeAgency(source, agency)
            collectAgencies(source, url_base, territorial_leaf, page_number + 1)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        logger.error('requests.exceptions.Timeout : ' + url)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        logger.error('requests.exceptions.TooManyRedirects: ' + url)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
        sys.exit(1)


def completeAllAgencies(source_name):
    """
    Complete the information of all the agencies that is_completed = False
    """
    logger.info("START Completing all Agencies for " + source_name + '. This will take a while...')
    source = Source.objects.get(source_name=source_name)
    for agency in Agency.objects.filter(is_completed=False):
        completeAgency(source, agency)


def getOrCreateAgencyLocalizationSource(source, code, url, localization):
    if len(code) == 1:
        agency_source_name = code[0].split('/')[2]
        agency_localization_source = AgencyLocalizationSource.objects.filter(source=source, agency_source_name=agency_source_name, agency_localization__in=AgencyLocalization.objects.filter(place=localization))
        # 0 AgencyLocationSource for that code and localization
        if len(agency_localization_source) == 0:
            list_agency_localization_source = AgencyLocalizationSource.objects.filter(source=source, agency_source_name=agency_source_name)
            # There is 0 agencies with that code in any localization
            if len(list_agency_localization_source) == 0:
                logger.warning('No AgencyLocationSource found for in ' + source.source_name + ' for the code ' + code[0] + ' in house url ' + url)
                return None
            # There is at least 1 agencies with that code but not with that localization
            else:
                agency = list_agency_localization_source.first().agency_localization.agency
                agency_localization = AgencyLocalization.objects.create(agency=agency, place=localization)
                return AgencyLocalizationSource.objects.create(agency_source_name=agency_source_name, agency_source_url=code[0], source=source, agency_localization=agency_localization)
        # 1 AgencyLocationSource for that code and localization
        elif len(agency_localization_source) == 1:
            return agency_localization_source[0]
        # >1 AgencyLocationSource for that code and localization
        else:
            logger.warning('More than 1 AgencyLocationSource found for in ' + source.source_name + ' for the code ' + code[0] + ' in house url ' + url)
            return None
    else:
        return None




def completeAgency(source, agency):
    """
    Complete all the information for a given agency in a source
    """
    if source.slug == 'id':
        # print(agency.agency_localization.all())
        local_agency = AgencyLocalization.objects.filter(agency=agency, place=agency.agency_localization.first())
        agency_localization = AgencyLocalizationSource.objects.filter(source=source, agency_localization=local_agency)
        if len(agency_localization) == 1:
            url = source.url + agency_localization[0].agency_source_url[1:]
            try:
                page = requests.get(url)
                tree = html.fromstring(page.content)
                # update the logo and web from the agency
                img = tree.xpath('//div[@class="logo-branding"]/img/@src')
                web = tree.xpath('//div[@id="online"]/a/@href')
                desc = tree.xpath('//p[@class="office-description"]/text()')
                if len(img) != 0:
                    agency.logo = img[0]
                if len(web) != 0:
                    print(web[0])
                    agency.url = web[0]
                if len(desc) != 0:
                    agency.desc = desc
                agency.save()
                # write local oh
                phone = tree.xpath('//*[@class="icon-phone"]/span/text()')
                address = ''.join(tree.xpath('//a[@class="showMap icon-location"]/div/span/text()'))
                if len(address) == 0:
                    address = ''.join(tree.xpath('//span[@class="regular-address"]/span/text()'))
                for territory in agency.agency_localization.all():
                    if len(phone) != 0:
                        territory.telephone = phone[0]
                        print(phone[0])
                    if len(address) != 0:
                        territory.address = address
                    territory.save()
                    # agency_localization = AgencyLocalizationSource.objects.filter(source=source, agency_localization=local_agency)
                checkCompleteAgencyFields(url, img, phone, web, desc, address)
                # print(img, phone, web, address)
            except requests.exceptions.Timeout:
                # Maybe set up for a retry, or continue in a retry loop
                logger.error('requests.exceptions.Timeout : ' + url)
            except requests.exceptions.TooManyRedirects:
                # Tell the user their URL was bad and try a different one
                logger.error('requests.exceptions.TooManyRedirects: ' + url)
            except requests.exceptions.RequestException as e:
                # catastrophic error. bail.
                logger.error('requests.exceptions.RequestException: ' + url + ', ' + e)
                sys.exit(1)
        else:
            logger.error('The query return more than un agency_localization')
    else:
        logger.warning('Only Idealista - Spain is implemented')


def checkCompleteAgencyFields(url, img, phone, web, desc, address):
    if len(img) == 0:
        # logger.warning('img didn´t import for: ' + url + ' agency.')
        pass
    # check: there are differents ways of represent the phone in Idealista
    if len(phone) == 0:
        logger.warning('phone didn´t import for: ' + url + ' agency.')
    if len(web) == 0:
        # logger.warning('web didn´t import for: ' + url + ' agency.')
        pass
    if len(desc) == 0:
        logger.warning('description didn´t import for: ' + url + ' agency.')
    if len(address) == 0:
        # logger.warning('address didn´t import for: ' + url + ' agency.')
        pass


def findAgenciesToMerge(agency):
    """
    Start a deduplicator process for a given agency and return a query of possible agencies to merge
    """
    pass
