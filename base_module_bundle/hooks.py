def post_init_hook(env):
    ir_module_module_obj = env["ir.module.module"]
    modules = ir_module_module_obj.sudo().search([])
    bundle_modules = ir_module_module_obj
    for module in modules:
        if module.get_module_info(module.name).get("bundle", False):
            bundle_modules += module
    bundle_modules.write({"module_type": "bundles"})
