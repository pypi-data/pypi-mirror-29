model_banks = [
    dict(
        order=0,
        code="f1",
        name="ForgeRock",
        support_url="https://www.forgerock.com",
        api_version="v1.1",
        postman_collections=["https://github.com/ForgeRock/ForgeRock-OpenBanking-Sample/tree/master/postman"],
        resource_server_endpoint="https://rs.aspsp.ob.forgerock.financial:443/open-banking/v1.1/",
        registration_endpoint="https://rs.aspsp.ob.forgerock.financial:443/open-banking/v1.1/registerTPP/",
        token_endpoint="https://as.aspsp.ob.forgerock.financial/oauth2/realms/root/realms/openbanking/access_token/",
        auth_endpoint="https://as.aspsp.ob.forgerock.financial/oauth2/realms/root/realms/openbanking/authorize",
        well_known="https://as.aspsp.ob.forgerock.financial/oauth2/.well-known/openid-configuration",
        discovery_endpoint="https://rs.aspsp.ob.forgerock.financial/open-banking/v1.1/discovery",

    ),
    dict(
        order=1,
        code="o31",
        name="Ozone",
        support_url="https://ob.o3bank.co.uk/",
        api_version="v1.1",
        postman_collections=[
            "https://ob.o3bank.co.uk/postman/O3-Heimdall.postman_collection.json",
            "https://ob.o3bank.co.uk/postman/OpenBanking-AISP-v1.1.0.postman_collection.json"
        ],
        resource_server_endpoint="https://modelobank.o3bank.co.uk:4101/open-banking/v1.1/",
        token_endpoint="https://modelobank.o3bank.co.uk:4501/token/",
        auth_endpoint="https://modelobankauth.o3bank.co.uk:4601/auth/",
        well_known="https://modelobankauth.o3bank.co.uk:4601/.well-known/openid-configuration",
        discovery_endpoint=None,

    )
]