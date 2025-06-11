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
    try:
        result = dns.resolver.resolve(inpDomainNameOrSomething, 'A')
    except dns.resolver.NoAnswer:
        print("\nDNS ERROR")
        print("No answer from dns server.\n")
        return 1
    except dns.resolver.NoNameservers:
        print("\nDNS ERROR")
        print("All nameservers failed to answer the query.\n Fix your DNS servers.\n")
        return 1
    except dns.resolver.NXDOMAIN:
        print("\nDNS ERROR")
        print("The DNS query name does not exist.\n")
        return 1
    except dns.resolver.LifetimeTimeout:
        print("\nDNS ERROR")
        print("The DNS querry got timed out.\nVerify that your FW or PiHole isn't blocking requests for that domain.\n")
        return 1
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
    try:
        result = dns.resolver.resolve(inpDomainNameOrSomething, 'AAAA')
    except dns.resolver.NoAnswer:
        print("\nDNS ERROR")
        print("No answer from dns server.\n")
        return 1
    except dns.resolver.NoNameservers:
        print("\nDNS ERROR")
        print("All nameservers failed to answer the query.\n Fix your DNS servers.\n")
        return 1
    except dns.resolver.NXDOMAIN:
        print("\nDNS ERROR")
        print("The DNS query name does not exist.\n")
        return 1
    except dns.resolver.LifetimeTimeout:
        print("\nDNS ERROR")
        print("The DNS querry got timed out.\nVerify that your FW or PiHole isn't blocking requests for that domain.\n")
        return 1
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
    try:
        result = dns.resolver.resolve(whatToCheck, 'PTR')
    except dns.resolver.NoAnswer:
        print("\nDNS ERROR")
        print("No answer from dns server.\n")
        return 1
    except dns.resolver.NoNameservers:
        print("\nDNS ERROR")
        print("All nameservers failed to answer the query.\n Fix your DNS servers.\n")
        return 1
    except dns.resolver.NXDOMAIN:
        print("\nDNS ERROR")
        print("The DNS query name does not exist.\n")
        return 1
    except dns.resolver.LifetimeTimeout:
        print("\nDNS ERROR")
        print("The DNS querry got timed out.\nVerify that your FW or PiHole isn't blocking requests for that domain.\n")
        return 1
    for i, something in enumerate(result):
        outDict[i] = something.to_text()
        # i += 1

    return outDict


#print(ermWhatATheIpFromDomainYaCrazy("fubukus.net"))
#print(ermWhatAAAATheIpFromDomainYaCrazy("fubukus.net"))
#print(ermWhatPTRTheIpFromDomainYaCrazy("192.168.1.226"))
