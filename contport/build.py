import jenkins
import url

def get_jenkins_home(job_url):
    myurl = url.parse(job_url)
    if myurl.port:
        return myurl.scheme + "://" + myurl.host + ":" + str(myurl.port)
    return myurl.scheme + "://" + myurl.host

def get_job_name(job_url):
    jenkins_home = get_jenkins_home(job_url)
    items = job_url.replace(jenkins_home, "").strip("/").split("job")
    return "/".join([i.strip("/") for i in items if i])

def get_jenkins_instance(job_url):
    jenkins_home = get_jenkins_home(job_url)
    return jenkins.Jenkins(jenkins_home)

def get_build_numbers(jenkins_instance, job_name, fetch_all_builds=False):
    result = jenkins_instance.get_job_info(job_name, fetch_all_builds=fetch_all_builds)
    return [i["number"] for i in result["builds"]]

def build_in_target():
    pass

def get_test_reports(job_url):
    test_reports = {}
    jenkins_instance = get_jenkins_instance(job_url)
    job_name = get_job_name(job_url)
    build_numbers = get_build_numbers(job_url)
    for number in build_numbers:
        report = jenkins_instance.get_build_test_report(job_name, number)
        print(report)
        


if __name__ == "__main__":
    #print(get_jenkins_home("http://xxx:8080/job/yyy/"))
    #print(get_jenkins_home("http://xxx/job/yyy/"))
    #print(get_job_name("http://xxx:8080/job/yyy/job/zzz"))
    print(get_test_reports("http://10.183.40.203:49001/job/test-robot-framework/"))
