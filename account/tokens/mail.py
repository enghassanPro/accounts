# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.timezone import now


# class MailTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self , user , timestamp):
        
#         return super()._make_hash_value(user , timestamp)

#     def make_token(self , user):
       
#         timestamp = int(str(now()).replace("-" , "").replace(" " , "").replace(":" , "").replace("." , "").split("+")[0])
       
#         return super()._make_token_with_timestamp(user , timestamp)



# mail_token = MailTokenGenerator()