# query-web3 quick start

## Install docker compose
 - [Install docker](https://docs.docker.com/engine/install/)
 - [Install docker compose](https://docs.docker.com/compose/install/)

## Run app
```sh
$ git clone https://github.com/Query-Web3/backend.git
$ cd backend/hacks
$ docker compose up
```

## Test api


 - Open address http://0.0.0.0:8082/

 - Input data and signature like this
    ```json
    query{
        yields(
            date: "",
            chain: "",
            asset: "",
            token: "",
            return: "",
            page: 1,
            size: 1000,
        ){
            total data
        }
    }
    ```

 - Click Execute button and check result has no error
    ```json
    {
     "data": {
        "yields": {
        "total": 13,
        "data": "[{\"id\":1,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"DOT\\\"}\",\"farm_apy\":0,\"pool_apy\":6.59,\"apy\":6.59,\"tvl\":12747883,\"volume\":920688,\"tx\":null,\"price\":1.854471,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":2,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"PHA\\\"}\",\"farm_apy\":0,\"pool_apy\":0,\"apy\":0,\"tvl\":0,\"volume\":0,\"tx\":null,\"price\":null,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":3,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"ASTR\\\"}\",\"farm_apy\":1.47,\"pool_apy\":6.49,\"apy\":7.96,\"tvl\":1778531,\"volume\":126465,\"tx\":null,\"price\":0.010147,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":4,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"ZTG\\\"}\",\"farm_apy\":0,\"pool_apy\":0.11,\"apy\":0.11,\"tvl\":75077,\"volume\":94,\"tx\":null,\"price\":null,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":5,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"CFG\\\"}\",\"farm_apy\":0,\"pool_apy\":3.45,\"apy\":3.45,\"tvl\":739191,\"volume\":27936,\"tx\":null,\"price\":null,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":6,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"BNC\\\"}\",\"farm_apy\":4.81,\"pool_apy\":0.59,\"apy\":5.4,\"tvl\":1006589,\"volume\":6485,\"tx\":null,\"price\":0.090584,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":7,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"vDOT\\\"}\",\"farm_apy\":0,\"pool_apy\":5.57,\"apy\":5.57,\"tvl\":3226980,\"volume\":197041,\"tx\":null,\"price\":2.898205,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":8,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"GLMR\\\"}\",\"farm_apy\":3.51,\"pool_apy\":3.47,\"apy\":6.98,\"tvl\":1365220,\"volume\":51880,\"tx\":null,\"price\":0.024199,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":9,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"INTR\\\"}\",\"farm_apy\":0,\"pool_apy\":2.22,\"apy\":2.22,\"tvl\":264479,\"volume\":6434,\"tx\":null,\"price\":0.00061,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":10,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"CRU\\\"}\",\"farm_apy\":0,\"pool_apy\":182.4,\"apy\":182.4,\"tvl\":48399,\"volume\":96745,\"tx\":null,\"price\":0.004517,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":11,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"KILT\\\"}\",\"farm_apy\":0,\"pool_apy\":2.47,\"apy\":2.47,\"tvl\":154591,\"volume\":4188,\"tx\":null,\"price\":null,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":12,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"vASTR\\\"}\",\"farm_apy\":0,\"pool_apy\":1.25,\"apy\":1.25,\"tvl\":378110,\"volume\":5170,\"tx\":null,\"price\":0.01369,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"},{\"id\":13,\"source\":\"hydration_data\",\"chain\":\"hydration\",\"batch_id\":1766223138,\"symbol\":\"{\\\"symbol\\\": \\\"TRAC\\\"}\",\"farm_apy\":11.02,\"pool_apy\":0,\"apy\":11.02,\"tvl\":0,\"volume\":0,\"tx\":null,\"price\":null,\"type\":null,\"return_type\":null,\"created_at\":\"2025-12-20T09:33:39Z\",\"inserted_at\":\"2025-12-20T09:36:55Z\"}]"
        }
    }
    }
    ```