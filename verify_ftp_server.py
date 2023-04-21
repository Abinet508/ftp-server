import ftplib, sys,os,random,argparse
class VerifyFTPServer():

    # Initialize the class
    def __init__(self, args):
        
        self.UploadedFile="TestUpload{}.txt".format(random.randint(1,100))
        self.DownloadedFile="TestDownload{}.txt".format(random.randint(1,100))
        self.LocalFile="test.txt"
        if len(args) == 0:
            print("No arguments passed")
            sys.exit(1)
        elif len(args) < 3 or len(args) > 3:
            print("Invalid number of arguments")
            sys.exit(1)
        else:
            
            self.ftp_host=args["ftp_host"]
            self.ftp_user=args["ftp_user"]
            self.ftp_pass=args["ftp_pass"]
            
            self.Connection=ftplib.FTP()
            self.Connection.connect(self.ftp_host,21)
            self.Connection.login(self.ftp_user, self.ftp_pass)
    
    # Create a local file For testing        
    def create_local_file(self):
        with open(self.LocalFile, "w") as f:
            f.write("This is a test file")
    
    # Upload the local file
    def upload_file(self):
        self.Connection.storbinary("STOR {}".format(self.UploadedFile), open(self.LocalFile, "rb"))
    
    # Download the uploaded file
    def download_file(self):
        self.Connection.retrbinary("RETR {}".format(self.UploadedFile), open(self.DownloadedFile, "wb").write)
    
    # Check if the uploaded file exists
    def check_upload_file(self):
        if self.Connection.nlst(self.UploadedFile):
            return True
        else:
            return False

    # Check if the downloaded file is not empty
    def check_download_file(self):
        if sys.getsizeof(self.DownloadedFile) > 0:
            return True
        else:
            return False

    # Delete all .txt files locally and remotely
    def delete_files(self):
        try:
            self.Connection.delete(self.LocalFile)
        except:
            pass
        
        try:
            for file in os.listdir(os.path.dirname(os.path.abspath(__file__))):
                if file.endswith(".txt"):
                    os.remove(file)
        except:  
            pass

    # Close the connection
    def close_connection(self):
        self.Connection.close()  

if __name__ == "__main__":
    MyArgs = argparse.ArgumentParser()
    MyArgs.add_argument("--ftp_host", help="FTP Host")
    MyArgs.add_argument("--ftp_user",help="FTP User")
    MyArgs.add_argument("--ftp_pass",help="FTP Password")
    
    Myobject=VerifyFTPServer(dict((MyArgs.parse_args()._get_kwargs()))) # Pass the arguments
    
    Myobject.create_local_file() # Create a local file For testing
    Myobject.upload_file() # Upload the local file
    Myobject.download_file() # Download the uploaded file

    if Myobject.check_upload_file() and Myobject.check_download_file(): # Check if the uploaded file exists and the downloaded file is not empty
        print("FTP server is working")
    else:
        raise Exception("FTP server is not working")

    Myobject.delete_files() # Delete all .txt files locally and remotely
    Myobject.close_connection() # Close the connection
  
