import jenkins
import url

def get_jenkins_home(job_url):
    myurl = url.parse(job_url)
    if myurl.port:
        return myurl.scheme + "://" + myurl.host + ":" + str(myurl.port)
    return myurl.scheme + "://" + myurl.host

if __name__ == "__main__":
    print(get_jenkins_home("http://mzoamci.eecloud.dynamic.nsn-net.net:8080/job/OAM_5GHZ_EIT_Regression\
    /job/5g.classicbts.master.oam.EIT-regression/"))
    print(get_jenkins_home("http://mzoamci.eecloud.dynamic.nsn-net.net/job/OAM_5GHZ_EIT_Regression\
    /job/5g.classicbts.master.oam.EIT-regression/"))
