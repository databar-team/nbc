# MAP Salesforce Marketing Cloud Worker

### Docker

Prerequisite: Login to Kasasa AWS container repository. This image is built on an image that is located there.

`$ $(aws ecr get-login --registry-ids 304872096477 --region us-west-2 | sed -e 's/-e none/ /g')`

#### Build

`$ docker build -t map-marketingcloud-sender .`

#### Run

`$ docker run -p 80:80 map-marketingcloud-sender`

#### Execute Tests

`$ make test`