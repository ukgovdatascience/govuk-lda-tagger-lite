"""
Custom pipeline for S3 Multi Part uploads
"""

# Origin: https://github.com/scrapy/scrapy/blob/bf7f67549378269c3976afc89abcf9c2190d242f/scrapy/extensions/feedexport.py#L94
# The below imports added by MU. Need to experiment with which others
# are not required.

import os
import math
import boto
from datetime import datetime
from filechunkio import FileChunkIO

settings = {
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY_ID": os.getenv("AWS_SECRET_ACCESS_KEY_ID"),
    "S3_BUCKET_NAME": os.getenv("S3_BUCKET_NAME"),
    "MULTIPART_CHUNK_SIZE": os.getenv("MULTIPART_CHUNK_SIZE"),
    "S3_DIR_NAME": os.getenv("S3_DIR_NAME")
    }

class S3MultiPartUploader(object):

    def __init__(self, file_name):

        self.file_name = file_name
        self.access_key = settings['AWS_ACCESS_KEY_ID']
        self.secret_key = settings['AWS_SECRET_ACCESS_KEY_ID']
        self.bucketname = settings['S3_BUCKET_NAME']
        self.connect_s3 = boto.connect_s3
        self.chunk_size = settings['MULTIPART_CHUNK_SIZE']
        self.s3_dir = settings['S3_DIR_NAME']

    def upload(self):

        conn = self.connect_s3(self.access_key, self.secret_key, host="s3.eu-west-2.amazonaws.com")
        bucket = conn.get_bucket(self.bucketname, validate=False)
                
        # First check filesize to decide on uploader to use
        # MUTLIPART_CHUNK_SIZE is given in MB
        # Must be above 10MB to use multi part uploaded (so use 10MB threshold)

        file_size = os.stat(self.file_name).st_size / 10e5
       
        if file_size > self.chunk_size:
            
            print("File size %s is bigger than chunk size: %s", file_size, self.chunk_size)
        
        # Create a multipart upload request
            try:
                mp = bucket.initiate_multipart_upload(os.path.join(self.s3_dir, self.file_name))
            except:
                print("Could not initiate multipart upload")
            else:
                print("Multipart upload initiated")
                
            chunk_count = int(math.ceil(file_size / float(self.chunk_size)))
            print("Uploading file as %s chunks", chunk_count)
            
            # Iterate through chunks
            # Send this to logger
                
            for i in range(chunk_count):
                print("Starting chunk %s...", i)
                
                offset = self.chunk_size * i
                
                bytes = min(self.chunk_size, file_size - offset)
                with FileChunkIO(self.file_name, 'r', offset=offset,bytes=bytes) as fp:
                    try:
                        mp.upload_part_from_file(fp, part_num=i + 1)
                    except:
                        print("Upload of chunk %s failed", i)
                    else:
                        print("Chunk %s complete", i)

            # Finish the upload.     
            # Note that if this step is not completed it is possible for uncompleted
            # multipart downloads to build up, but not be visible.
            # Run bucket.get_all_multipart_uploads() to see...
                
            try:        
                mp.complete_upload()
            except:
                print("Failed to complete multi-part upload, consider checking for orphans!")
                print(sys.exc_info[0])
            else:
                print("Multipart upload complete")
            
        # If file is not big enough to use mp uploader, use the standard uplaoder
   
        else:
            print("File size %s is smaller than chunk size: %s, so uploading as single chunk", file_size, self.chunk_size)

            k = boto.s3.key.Key(bucket)
            k.key = os.path.join(self.s3_dir, self.file_name)
            k.set_contents_from_filename(self.file_name)
            k.close()
            print("Single chunk upload complete")
