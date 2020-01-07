import yaml

with open('proxy_config_atlas.yaml', 'r') as stream:
    proxy_config = yaml.safe_load(stream)

proxy_config['service_uris']['foundations_rest_api'] = 'http://localhost:37722'

with open('proxy_config_atlas.yaml', 'w') as outfile:
    yaml.dump(proxy_config, outfile, default_flow_style=False)