# coding=utf-8
from __future__ import absolute_import

import unittest

from helpers import xroad
from main.maincontroller import MainController
from tests.xroad_add_to_acl_from_client_219 import add_to_acl_client as test_add_to_acl_client
from tests.xroad_configure_service_222 import configure_service
from tests.xroad_parse_users_inputs import xroad_parse_user_inputs
from tests.xroad_ss_client.ss_client_management import edit_client
from view_models import clients_table_vm
from view_models.messages import get_error_message


class XroadAddToAclFromClient(unittest.TestCase):
    """
    SERVICE_01 View the Service Clients of a Security Server Client
    SERVICE_02 View the Access Rights of a Service Client
    SERVICE_03 Add Access Rights for a Service Client
    SERVICE_05 Remove Access Rights from a Service Client
    RIA URL: https://jira.ria.ee/browse/XT-258, https://jira.ria.ee/browse/XTKB-166
    RIA URL: https://jira.ria.ee/browse/XT-259, https://jira.ria.ee/browse/XTKB-167
    RIA URL: https://jira.ria.ee/browse/XT-260, https://jira.ria.ee/browse/XTKB-78
    RIA URL: https://jira.ria.ee/browse/XT-262, https://jira.ria.ee/browse/XTKB-81
    Depends on finishing other test(s): XroadSecurityServerClientRegistration, XroadConfigureService
    Requires helper scenarios:
    X-Road version: 6.16.0
    """

    def test_acl(self):
        main = MainController(self)

        main.test_number = 'SERVICE_01/02/03/05'
        main.test_name = self.__class__.__name__

        ss_host = main.config.get('ss1.host')
        ss_user = main.config.get('ss1.user')
        ss_pass = main.config.get('ss1.pass')

        ss_ssh_host = main.config.get('ss1.ssh_host')
        ss_ssh_user = main.config.get('ss1.ssh_user')
        ss_ssh_pass = main.config.get('ss1.ssh_pass')

        client_name = main.config.get('ss1.client_name')
        client_id = xroad.split_xroad_id(main.config.get('ss1.client_id'))

        wsdl_three_services = main.config.get('wsdl.remote_path').format('three_services.wsdl')

        test_add_to_1_client = test_add_to_acl_client.test_empty_client(ss_ssh_host, ss_ssh_user, ss_ssh_pass, [1],
                                                                        remove_data=True, client_name=client_name,
                                                                        view_service_clients=True)
        test_add_list_of_services = test_add_to_acl_client.test_empty_client(rows_to_select=[1, 2], remove_data=True,
                                                                             client_name=client_name)
        test_add_all_services = test_add_to_acl_client.test_empty_client(rows_to_select=0, remove_data=True,
                                                                         client_name=client_name)
        test_add_1_client_to_existing = test_add_to_acl_client.test_existing_client(ss_ssh_host=ss_ssh_host,
                                                                                    ss_ssh_user=ss_ssh_user,
                                                                                    ss_ssh_pass=ss_ssh_pass,
                                                                                    rows_to_select=[[1], [2]],
                                                                                    remove_data=True,
                                                                                    client_name=client_name)
        test_add_list_of_services_to_existing = test_add_to_acl_client.test_existing_client(
            rows_to_select=[[1], [2, 3]], remove_data=True, client_name=client_name)
        test_add_all_service_to_existing = test_add_to_acl_client.test_existing_client(rows_to_select=[[1], [0]],
                                                                                       remove_data=True,
                                                                                       client_name=client_name)
        delete_added_wsdl = configure_service.test_delete_service(main, client_name=client_name,
                                                                  client_id=client_id,
                                                                  wsdl_url=wsdl_three_services)
        try:
            main.log('Add WSDL with 3 services to security server client')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            row = clients_table_vm.get_client_row_element(self=main, client_name=client_name)
            edit_client(main, row)
            xroad_parse_user_inputs.add_wsdl_url(main, wsdl_three_services)
            main.is_none(get_error_message(main))

            main.log('SERVICE_03 Add a service client to a security server client(1 service)')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_add_to_1_client(main)

            main.log('SERVICE_03 Add a service client to a security server client(list of services)')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_add_list_of_services(main)

            main.log('SERVICE_03 Add a service client to a security server client(all services)')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_add_all_services(main)

            main.log('SERVICE_04 Add access rights for a service client(1 service)')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_add_1_client_to_existing(main)

            main.log('SERVICE_04 Add access rights for a service client(list of services)')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_add_list_of_services_to_existing(main)

            main.log('SERVICE_04 Add access rights for a service client(all services)')
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            test_add_all_service_to_existing(main)
        except:
            main.save_exception_data()
            raise
        finally:
            main.reload_webdriver(ss_host, ss_user, ss_pass)
            delete_added_wsdl()
            main.tearDown()
