#from nslookup import Nslookup
from typing import Optional, Annotated
import dns, dns.resolver

# https://www.codeunderscored.com/nslookup-python/

def ermWhatATheIpFromDomainYaCrazy(inpDomainNameOrSomething: Annotated[str, "Domain name to lookup IP for"]):
    #dns_query = Nslookup()
    """
    Tells you what IPv4 address/es a domain point to.
    Returns:
        dict: A dictionary with IP addresses associated with that domain.

    """

    # i = 0
    outDict = {} 

    #result = dns_query.dns_lookup("example.com")
    #result = Nslookup.dns_lookup(inpDomainNameOrSomething)
    result = dns.resolver.resolve(inpDomainNameOrSomething, 'A')
    for i, something in enumerate(result):
        outDict[i] = something.to_text()
        # i += 1

    return outDict

def ermWhatAAAATheIpFromDomainYaCrazy(inpDomainNameOrSomething: Annotated[str, "Domain name to lookup IP for"]):
    #dns_query = Nslookup()
    """
    Tells you what IPv6 address/es a domain point to.
    Returns:
        dict: A dictionary with IP addresses associated with that domain.

    """


    # i = 0
    outDict = {} 

    #result = dns_query.dns_lookup("example.com")
    #result = Nslookup.dns_lookup(inpDomainNameOrSomething)
    result = dns.resolver.resolve(inpDomainNameOrSomething, 'AAAA')
    for i, something in enumerate(result):
        outDict[i] = something.to_text()
        # i += 1

    return outDict


def ermWhatPTRTheIpFromDomainYaCrazy(inpIpAddressOrSomething: Annotated[str, "IP address to lookup domain for"]):
    #dns_query = Nslookup()
    """
    Tells you what IPv6 address/es a domain point to.
    Returns:
        dict: A dictionary with IP addresses associated with that domain.

    """

    whatToCheck = inpIpAddressOrSomething + ".in-addr.arpa"


    # i = 0
    outDict = {}

    #result = dns_query.dns_lookup("example.com")
    #result = Nslookup.dns_lookup(inpDomainNameOrSomething)
    result = dns.resolver.resolve(whatToCheck, 'PTR')
    for i, something in enumerate(result):
        outDict[i] = something.to_text()
        # i += 1

    return outDict


#print(ermWhatATheIpFromDomainYaCrazy("fubukus.net"))
#print(ermWhatAAAATheIpFromDomainYaCrazy("fubukus.net"))
#print(ermWhatPTRTheIpFromDomainYaCrazy("192.168.1.226"))
