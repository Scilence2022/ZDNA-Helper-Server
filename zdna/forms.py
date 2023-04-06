from django import forms

class UpdatePassForm(forms.Form):
    md5pass = forms.CharField(label='MD5 value of your old password: ', max_length=100)
    md5newpass = forms.CharField(label='MD5 value of your new password:', max_length=100)
    md5data = forms.CharField(label='MD5 value of your NFT data:', max_length=100)
    xor2pass = forms.CharField(label='XOR value of your old and new password:', max_length=100)



class EncryptionPassForm(forms.Form):
    # title = forms.CharField(max_length=50)
    md5pass = forms.CharField(label='MD5 value of your password: ', max_length=100)
    file = forms.FileField(label='The NFT meta data encrypted with your password')

class DecryptionPassForm(forms.Form):
    # title = forms.CharField(max_length=50)
    md5pass = forms.CharField(label='MD5 value of your password: ', max_length=100)
    file = forms.FileField(label='The encrypted NFT meta data file')
