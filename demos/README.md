# Proxy
This demonstration shows how to establish a **proxy** end-2-end demo for the MyPCH project. 

It will describe and demo how components from Semantic Container (SC) can be integrated into the Tidepool platform (TP).

We have defined a concept of a health-datastore (HDS) to merit higher protection for sensitive data as health data. The HDS is inspired by similar examples using human-centric MyData principles in https://github.com/okffi/mydata#9---give-me-some-examples. 

The proxy is a data integration to Tidepool as a proxy to handle integration between TP uploader, SC-features and a HDS-backend as Tidepool platform. In the code it is marked where it is possible to make a SC-hook to demonstrate how features from an extended SC-framework can enhance PwD diabetes data with features like watermarking, anonymization, provenance and features to make a granular consent by use of usages policy.  
 
## Overview 
- [Local demo](proxy/README.md)
- [Online demo](proxy/README.md)
    - [Tidepool](prepare/getstarted.md#tidepool)




xxx
A service that lack these fundamental properties will be able to integrate with the platform either directly by extending the proxy itself or indirectly by using the API of the proxy in their integration of the service.

We have defined a concept of a health-datastore (HDS) to merit higher protection for sensitive data as health data. The HDS is inspired by similar examples of human-centric MyData principles in https://github.com/okffi/mydata#9---give-me-some-examples. 

IFor WP3 we have deliver a data integration to Tidepool as a proxy to handle integration between uploader, SC and a HDS-backend as Tidepool platform. In the code it is marked where it is possible to make a SC-hook to demonstrate how features from an extended SC-framework can enhance PwD diabetes data with features like watermarking, anonymization, provenance and features to make a granular consent by use of usages policy.  
 
	ð Please elaborate on what we can expect of delivery from WorkPackage WP3 with installation script and how it can be available in WP5 for the use case implementation that can demonstrate the integration of any implemented SC features for sharing with others in a multi-user environment
 
If you have other ideas of making a integration demo script for any SC features, please let us know.


This directory shows how to establish an end-2-end demo for the MyPCH project allowing the project to deliver on the use case 3 from the proposal. It will demo how e.g. SCs can be integrated into the TP platform and it deals with the two gaps (authentification and encryption of data at rest) that were revealed during the initial analysis pertaining to the specification of the requirement. A service that lack these fundamental properties will be able to integrate with the platform either directly by extending the proxy itself or indirectly by using the API of the proxy in their integration of the service.



