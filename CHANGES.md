0.1.0 (2020-12-03)
------------------
* Initial release

0.2.0 (2020-12-04)
------------------
* Implement the boto3 filter tags
* Implement the flask logging
* Add the Dockerfile

0.3.0 (2020-12-07)
------------------
* Add unit test

0.4.0 (2020-12-08)
------------------
* Update the api endpoint
* Update the Dockerfile

0.5.0 (2020-12-09)
------------------
* Implement the tinydb json
* Update the sorting and query result

0.6.0 (2020-12-10)
------------------
* Adding prometheus metrics

0.7.0 (2020-12-10)
------------------
* Bug fix, send logs if API cannot connect to cloud provider

0.8.0 (2020-12-17)
------------------
* Add GCP Provider

0.9.0 (2020-12-31)
------------------
* Add Azure Provider

0.10.0 (2021-01-04)
-------------------
* List images on Azure
* Add lines to update table if there's new changes in the image tags/labels

0.11.0 (2021-01-04)
-------------------
* Finalized the unit test

0.11.1 (2021-01-05)
-------------------
* Bug fix for azure images to query both 'rhel' and 'redhat' as the same OS

0.11.2 (2021-01-22)
-------------------
* Set environment variable to choose which cloud provider that the API able to list the images