
import pickle
import itertools
import os
import random
import pickle

class parallel_runner():
    def __init__(self,ini_dir="./ini/",result_dir="./results/",max_error_times=5,if_log=False):
        if ini_dir[-1]!="/":
            ini_dir+="/"
        if result_dir[-1]!="/":
            result_dir+="/"
        self.ini_dir=ini_dir
        self.max_error_times=max_error_times
        self.result_dir=result_dir
        if os.path.exists(self.result_dir):
            os.mkdir(self.result_dir)
        self.if_log=if_log
        pass
    
    def generate_ini(self,args_list,reserve_old_ini=True,show_ini=False):
        if not os.path.exists(self.ini_dir):
            os.mkdir(self.ini_dir)
        else:
            if len(os.listdir(self.ini_dir))>0:
                if reserve_old_ini:
                    if self.if_log:
                        print "Ini files already generated."
                    return
                else:
                    if self.if_log:
                        print "There are old ini files to be deleted.\nPlease delete the old ini files manually and try again."
                    return
        count=1
        for i in itertools.product(*args_list):
            if show_ini:
                print i
            pickle.dump(i,open(self.ini_dir+str(count)+"_to_run","w"))
            count+=1
        count-=1
        if self.if_log:
            print "All "+str(count)+" ini files generated."
        
    def find_files(self,_type):
        all_files=filter(lambda x:x[0]!=".",os.listdir(self.ini_dir))
        return filter(lambda x:x[-len(_type):]==_type,all_files)
        
    def return_a_para(self):
        this_para=[]
        while(this_para==[] and len(self.find_files("_to_run"))>0):
            choises=self.find_files("_to_run")
            if len(choises)==0:
                return [],-1
            else:
                my_choise=choises[random.randint(0,len(choises)-1)]
                new_name=self.ini_dir+my_choise[:-7]+"_running"
                try:
                    os.rename(self.ini_dir+my_choise,new_name)      
                    this_para=pickle.load(open(new_name,"r"))
                    return this_para,new_name
                except OSError:
                    pass
        return [],-1
    
    def run(self,main_function):
        error_time=0
        while(error_time<self.max_error_times): 
            find_a_para,para_path=self.return_a_para()
            if find_a_para==[]:
                if self.if_log:
                    print "No new task to run."
                break
            else:
                try:
                    result=main_function(find_a_para)
                    pickle.dump(result,open(self.result_dir+para_path[len(self.ini_dir):-8],"w"))
                    os.rename(para_path,para_path[:-8]+"_finished")   
                except Exception:
                    error_time+=1
                    os.rename(para_path,para_path[:-8]+"_to_run")
            if error_time>=self.max_error_times:
                if self.if_log:
                    print "Too many error times, break."
