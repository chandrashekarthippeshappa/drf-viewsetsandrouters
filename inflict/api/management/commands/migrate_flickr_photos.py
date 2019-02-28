try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand
    
import time,json
import requests
import urllib.request
from api.models import Group,Photo
from django.contrib.auth.models import User
from django.core.files import File



class Command(BaseCommand):
    help="""        
        This command is for saving photos in local system and upload to DB.
        use like : python manage.py migrate_flickr_photos username
    """
    def add_arguments(self, parser):
        parser.add_argument('username')
        
    def handle(self, *args, **options):
        def pr_red(prt): print("\033[91m {}\033[00m" .format(prt))
        def pr_yellow(prt): print("\033[93m {}\033[00m" .format(prt))
        def pr_green(prt): print("\033[92m {}\033[00m" .format(prt))
        pr_red("cron Start.....")
        start_time = time.time()
        def prYellow(prt): print("\033[93m {}\033[00m" .format(prt))
        pr_yellow("Starting Time:"+str(start_time))
        if options['username']:
            username = options['username']
        else:
            self.prRed("Recruiter ID is mandatory")
            return
        main(username)
        pr_red("cron End.....")
        end_time = time.time()
        pr_yellow("Ended Time:"+str(end_time))
        total_time = end_time - start_time 
        if total_time > 60:
            total_time = total_time/60
            def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
            pr_green("Total time taken:"+str(round(total_time, 2))+"Minuts")
        else:
            def prGreen(prt): print("\033[92m {}\033[00m" .format(prt))
            pr_green("Total time taken:"+str(round(total_time, 2))+"Seconds") 
            
def main(username):
    try:
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            err =  {'comment': 'user does not exists'}
            print(err)
            return 
        url = "https://api.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=5249c9db5797c29af874379ac27ee5e2&group_id=80641914%40N00+&format=json&nojsoncallback=1&page=1&per_page=100"
        result = requests.get(url = url)
        data = eval(result.content)
        count1 = 100
        if result.status_code >=200 and result.status_code<299:
            if data['stat'] == 'ok' and data['photos']['photo']:
                for image in data['photos']['photo']:
                    if count1%25==0:
                        group_name = str(input("input group name: "))
                        while check_group_exits(group_name):
                            group_name = str(input("enter unique group name: "))
                        group = Group.objects.create(user = user,group_name =group_name)
                    count1 +=1
                    print(count1)   
                    farm = image['farm']
                    server = image['server']
                    id = image['id']
                    secret = image['secret']
                    url = "http://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg".format(farm,server,id,secret)
                    image_name ="inflict_{}.jpg".format(str(count1).zfill(5))
                    urllib.request.urlretrieve(url, "./downloads/{}".format(image_name))
                    Photo.objects.create(group = group,photo_name = image_name,photo = File(open('./downloads/{}'.format(image_name), 'rb')))
                          
            else:
                err =  {'status': result.status_code,'content':result.content,'comment':'unable to images'}
                raise Exception(err)
        else:
            err =  {'status': result.status_code,'content':result.content,'comment': 'unable to fetch images error occured'}
            raise Exception(err)
                     
    except Exception as err:
        raise Exception(err)
    
def check_group_exits(group_name):
    group = Group.objects.filter(group_name = group_name)
    if group:
        return True
    return False
    
    
    
        
    

    
    
    