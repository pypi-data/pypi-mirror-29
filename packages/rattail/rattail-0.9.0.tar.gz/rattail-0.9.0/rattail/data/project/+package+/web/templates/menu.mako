## -*- coding: utf-8 -*-

<%def name="main_menu_items()">

    % if request.has_any_perm('products.list', 'brands.list', 'reportcodes.list'):
        <li>
          <a>Products</a>
          <ul>
            % if request.has_perm('products.list'):
                <li>${h.link_to("Products", url('products'))}</li>
            % endif
            % if request.has_perm('brands.list'):
                <li>${h.link_to("Brands", url('brands'))}</li>
            % endif
            % if request.has_perm('reportcodes.list'):
                <li>${h.link_to("Report Codes", url('reportcodes'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('vendors.list', 'vendorcatalogs.list', 'vendorcatalogs.create'):
        <li>
          <a>Vendors</a>
          <ul>
            % if request.has_perm('vendors.list'):
                <li>${h.link_to("Vendors", url('vendors'))}</li>
            % endif
            % if request.has_any_perm('vendorcatalogs.list', 'vendorcatalogs.create'):
                <li>-</li>
                % if request.has_perm('vendorcatalogs.list'):
                    <li>${h.link_to("Catalogs", url('vendorcatalogs'))}</li>
                % endif
                % if request.has_perm('vendorcatalogs.create'):
                    <li>${h.link_to("Upload New Catalog", url('vendorcatalogs.create'))}</li>
                % endif
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('stores.list', 'departments.list', 'subdepartments.list', 'employees.list', 'customers.list', 'customergroups.list'):
        <li>
          <a>Company</a>
          <ul>
            % if request.has_perm('stores.list'):
                <li>${h.link_to("Stores", url('stores'))}</li>
            % endif
            % if request.has_perm('departments.list'):
                <li>${h.link_to("Departments", url('departments'))}</li>
            % endif
            % if request.has_perm('subdepartments.list'):
                <li>${h.link_to("Subdepartments", url('subdepartments'))}</li>
            % endif
            % if request.has_perm('employees.list'):
                <li>-</li>
                <li>${h.link_to("Employees", url('employees'))}</li>
            % endif
            % if request.has_any_perm('customers.list', 'customergroups.list'):
                <li>-</li>
                % if request.has_perm('customers.list'):
                    <li>${h.link_to("Customers", url('customers'))}</li>
                % endif
                % if request.has_perm('customergroups.list'):
                    <li>${h.link_to("Customer Groups", url('customergroups'))}</li>
                % endif
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('batch.handheld.list', 'batch.inventory.list'):
        <li>
          <a>Batches</a>
          <ul>
            % if request.has_perm('batch.handheld.list'):
                <li>${h.link_to("Handheld", url('batch.handheld'))}</li>
            % endif
            % if request.has_perm('batch.inventory.list'):
                <li>${h.link_to("Inventory", url('batch.inventory'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.has_any_perm('users.list', 'roles.list', 'settings.list', 'emailprofiles.list', 'datasyncchanges.list'):
        <li>
          <a>Admin</a>
          <ul>
            % if request.has_perm('users.list'):
                <li>${h.link_to("Users", url('users'))}</li>
            % endif
            % if request.has_perm('roles.list'):
                <li>${h.link_to("Roles", url('roles'))}</li>
            % endif
            % if request.has_perm('settings.list'):
                <li>${h.link_to("Settings", url('settings'))}</li>
            % endif
            % if request.has_perm('emailprofiles.list'):
                <li>${h.link_to("Email Profiles", url('emailprofiles'))}</li>
            % endif
            % if request.has_perm('datasyncchanges.list'):
                <li>${h.link_to("DataSync Changes", url('datasyncchanges'))}</li>
            % endif
          </ul>
        </li>
    % endif

    % if request.user:
        <li>
          <a${' class="root-user"' if request.is_root else ''|n}>${request.user}${" ({})".format(inbox_count) if inbox_count else ''}</a>
          <ul>
            % if request.is_root:
                <li class="root-user">${h.link_to("Stop being root", url('stop_root'))}</li>
            % elif request.is_admin:
                <li class="root-user">${h.link_to("Become root", url('become_root'))}</li>
            % endif
            <li>${h.link_to("Messages{}".format(" ({})".format(inbox_count) if inbox_count else ''), url('messages.inbox'))}</li>
            <li>${h.link_to("Change Password", url('change_password'))}</li>
            <li>${h.link_to("Logout", url('logout'))}</li>
          </ul>
        </li>
    % else:
        <li>${h.link_to("Login", url('login'))}</li>
    % endif

</%def>
