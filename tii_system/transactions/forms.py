from datetime import datetime
from django import forms
from transactions.models import Transaction
from crispy_forms.helper import FormHelper

TERM_CHOICES = (
    ('' , '-- Choose Year --'),
    ('0 Year', '0 Year'),
    ('1 Year', '1 Year'),
    ('2 Year', '2 Year'),
    ('3 Year', '3 Year'),
    ('4 Year', '4 Year'),
    ('5 Year', '5 Year'),
    ('6 Year', '6 Year'),
    ('7 Year', '7 Year'),
    ('8 Year', '8 Year'),
    ('9 Year', '9 Year'),
    ('10 Year', '10 Year'),
    ('11 Year', '11 Year'),
    ('12 Year', '12 Year'),
    ('13 Year', '13 Year'),
    ('14 Year', '14 Year'),
    ('15 Year', '15 Year'),
    ('16 Year', '16 Year'),
    ('17 Year', '17 Year'),
    ('18 Year', '18 Year'),
    ('19 Year', '19 Year'),
    ('20 Year', '20 Year'),
)

TERM_UNIT_CHOICES = (
    ('' , '-- Choose Month --'),
    ('0 Month', '0 Month'),
    ('1 Month', '1 Month'),
    ('2 Month', '2 Month'),
    ('3 Month', '3 Month'),
    ('4 Month', '4 Month'),
    ('5 Month', '5 Month'),
    ('6 Month', '6 Month'),
    ('7 Month', '7 Month'),
    ('8 Month', '8 Month'),
    ('9 Month', '9 Month'),
    ('10 Month', '10 Month'),
    ('11 Month', '11 Month'),
    ('12 Month', '12 Month'),
)

LEGAL_STATUS_CHOICES = (
    ('' , '-- Choose Status --'),
    ('Proprietary', 'Proprietary'),
    ('LLC', 'LLC'),
    ('Incorporated', 'Incorporated'),
)

def possible_years(first_year, last_year):

    p_year = []
    p_year.append(('' , '-- Choose Year --'))
    for i in range(first_year, last_year, -1):
        p_year_tuple = str(i), i
        p_year.append(p_year_tuple)

    return p_year


class Representative_Us_CompanyForm(forms.ModelForm):
    comp_us_name            = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company name here'}),
                                label='Name of Company')

    comp_us_president       = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert name of the person in charge of your (XA) company here'}),
                                label='Name of Company President')

    comp_us_legal_status    = forms.ChoiceField(
                                widget=forms.Select(
                                attrs={'onfocus':'this.size=4;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'},),
                                choices=LEGAL_STATUS_CHOICES,
                                label='Legal Form Status')

    comp_us_establishment   = forms.ChoiceField(
                                widget=forms.Select(
                                attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                choices=possible_years(((datetime.now()).year),1800),
                                label='Year Of establishment')

    comp_us_address         = forms.CharField(
                                widget=forms.Textarea(
                                attrs={'placeholder':'Please insert the address of your (XA) company here', 'rows':'5', 'style':'resize: none;'}),
                                label='Headquarter Address')

    comp_us_state           = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'state'}),
                                label='Headquarter state')

    comp_us_city            = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'city'}),
                                label='Headquarter city')

    comp_us_zip             = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'zip code'}),
                                label='Headquarter zip code')

    comp_us_website         = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': '(e.g. www.YourCompany.com)'}),
                                label='Website')

    comp_us_phone           = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'phone number'}),
                                label='Phone No.')

    comp_us_fax             = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'fax number'}),
                                label='Fax No.')

    comp_us_email           = forms.EmailField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company email address here',
                                'aria-describedby':'emailHint'}),
                                label='Email address')

    line_of_business        = forms.CharField(
                                widget=forms.TextInput(
                                attrs= {'placeholder': 'Please insert your (XA) company line of business here'}),
                                label='Line of Business')

    product_offering        = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company products or services offered here'}),
                                label='Product/Service Offerings')

    cert_good_standing      = forms.FileField(
                                widget=forms.ClearableFileInput(
                                attrs=  {'type': 'file',
                                'aria-describedby':'cgsHelp'}),
                                label='Upload Certificate of Good Standing')


    class Meta:
        model = Transaction
        fields =(
            'comp_us_name',
            'comp_us_president',
            'comp_us_website',
            'comp_us_legal_status',
            'comp_us_establishment',
            'comp_us_address',
            'comp_us_city',
            'comp_us_state',
            'comp_us_zip',
            'comp_us_phone',
            'comp_us_fax',
            'comp_us_email',
            'cert_good_standing',
            'line_of_business',
            'product_offering',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.help_text_inline = False
        self.fields['comp_us_fax'].required = False
        self.fields['comp_us_website'].required = False


class Representative_Id_CompanyForm(forms.ModelForm):
    comp_idn_name           = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert XB company name here'}),
                                    label='Name of XB Company')

    comp_idn_president      = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert name of the person in charge of your (XB) company here'}),
                                    label='Name of XB Company President')

    comp_idn_address        = forms.CharField(
                                    widget=forms.Textarea(
                                    attrs={'placeholder':'Please insert the address of XB company here', 'rows':'5', 'style':'resize: none;'}),
                                    label='Address of XB Company')

    comp_idn_province       = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the Province of XB company here'}),
                                    label='Province of XB Company')

    comp_idn_city           = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the City of XB company here'}),
                                    label='City of XB Company')

    comp_idn_zip            = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the Zip Code of XB company here'}),
                                    label='Zip Code of XB Company')

    comp_idn_website        = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': '(e.g. www.YourCompany.com)'}),
                                    label='Website')

    comp_idn_phone          = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert phone number of XB company here'}),
                                    label='Phone No. (IDN)')

    comp_idn_fax            = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert fax number of XB company here'}),
                                    label='Fax No. (IDN)')

    comp_idn_email          = forms.EmailField(
                                    widget=forms.EmailInput(
                                    attrs={'placeholder': 'Please insert your XB company email address here'}),
                                    label='Email address')

    term                    = forms.ChoiceField(
                                    widget=forms.Select(
                                    attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                    choices = TERM_CHOICES,
                                    label='Term')

    term_unit               = forms.ChoiceField(
                                    widget=forms.Select(
                                    attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                    choices = TERM_UNIT_CHOICES,
                                    label='Term Unit')

    comp_idn_nationality    = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer nationality here'}),
                                    label='Nationality Representative Officer of XB Company')

    comp_idn_idnumber       = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer identity card number here'}),
                                    label='Identity Card Number Representative Officer of XB Company')

    comp_idn_rep_officer    = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer name here'}),
                                    label='Name Representative Officer of XB Company')

    loi                     = forms.FileField(
                                    widget=forms.ClearableFileInput(
                                    attrs={'type': 'file',
                                            'aria-describedby':'loiHelp'}),
                                    label='LoI')

    loa                     = forms.FileField(
                                    widget=forms.ClearableFileInput(
                                    attrs={'type': 'file',
                                            'aria-describedby':'loaHelp'}),
                                    label='LoA')

    los                     = forms.FileField(
                                    widget=forms.ClearableFileInput(
                                    attrs={'type': 'file',
                                            'aria-describedby':'losHelp'}),
                                    label='LoS')


    class Meta:
        model = Transaction
        fields = (
            'comp_idn_name',
            'comp_idn_president',
            'comp_idn_address',
            'comp_idn_city',
            'comp_idn_province',
            'comp_idn_zip',
            'comp_idn_phone',
            'comp_idn_fax',
            'comp_idn_email',
            'comp_idn_website',
            'comp_idn_nationality',
            'comp_idn_idnumber',
            'comp_idn_rep_officer',
            'term',
            'term_unit',
            'contractual_agreement',
            'prospectus_agreement',
            'loi',
            'loa',
            'los',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['comp_idn_fax'].required = False
        self.fields['comp_idn_website'].required = False
        self.fields['comp_idn_president'].required = False


class Agent_Distributor_Us_CompanyForm(forms.ModelForm):
    comp_us_name            = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company name here'}),
                                label='Name of Company')

    comp_us_president       = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert name of the person in charge of your (XA) company here'}),
                                label='Name of Company President')

    comp_us_legal_status    = forms.ChoiceField(
                                widget=forms.Select(
                                attrs={'onfocus':'this.size=4;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'},),
                                choices=LEGAL_STATUS_CHOICES,
                                label='Legal Form Status')

    comp_us_establishment   = forms.ChoiceField(
                                widget=forms.Select(
                                attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                choices=possible_years(((datetime.now()).year),1800),
                                label='Year Of establishment')

    comp_us_address         = forms.CharField(
                                widget=forms.Textarea(
                                attrs={'placeholder':'Please insert the address of your (XA) company here', 'rows':'5', 'style':'resize: none;'}),
                                label='Headquarter Address')

    comp_us_state           = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'state'}),
                                label='Headquarter state')

    comp_us_city            = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'city'}),
                                label='Headquarter city')

    comp_us_zip             = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'zip code'}),
                                label='Headquarter zip code')

    comp_us_website         = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': '(e.g. www.YourCompany.com)'}),
                                label='Website')

    comp_us_phone           = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'phone number'}),
                                label='Phone No.')

    comp_us_fax             = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'fax number'}),
                                label='Fax No.')

    comp_us_email           = forms.EmailField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company email address here',
                                'aria-describedby':'emailHint'}),
                                label='Email address')

    line_of_business        = forms.CharField(
                                widget=forms.TextInput(
                                attrs= {'placeholder': 'Please insert your (XA) company line of business here'}),
                                label='Line of Business')

    product_offering        = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company products or services offered here'}),
                                label='Product/Service Offerings')

    hs_code                 = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company HS Code products or services offered here'}),
                                label='HS Code Product/Service Offerings')

    cert_good_standing      = forms.FileField(
                                widget=forms.ClearableFileInput(
                                attrs=  {'type': 'file',
                                'aria-describedby':'cgsHelp'}),
                                label='Upload Certificate of Good Standing')


    class Meta:
        model = Transaction
        fields =(
            'comp_us_name',
            'comp_us_president',
            'comp_us_website',
            'comp_us_legal_status',
            'comp_us_establishment',
            'comp_us_address',
            'comp_us_city',
            'comp_us_state',
            'comp_us_zip',
            'comp_us_phone',
            'comp_us_fax',
            'comp_us_email',
            'cert_good_standing',
            'line_of_business',
            'product_offering',
            'hs_code',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.help_text_inline = False
        self.fields['comp_us_fax'].required = False
        self.fields['comp_us_website'].required = False


class Agent_Distributor_Id_CompanyForm(forms.ModelForm):
    comp_idn_name           = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert XB company name here'}),
                                    label='Name of XB Company')

    comp_idn_president      = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert name of the person in charge of your (XB) company here'}),
                                    label='Name of XB Company President')

    comp_idn_address        = forms.CharField(
                                    widget=forms.Textarea(
                                    attrs={'placeholder':'Please insert the address of XB company here', 'rows':'5', 'style':'resize: none;'}),
                                    label='Address of XB Company')

    comp_idn_province       = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the Province of XB company here'}),
                                    label='Province of XB Company')

    comp_idn_city           = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the City of XB company here'}),
                                    label='City of XB Company')

    comp_idn_zip            = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the Zip Code of XB company here'}),
                                    label='Zip Code of XB Company')

    comp_idn_website        = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': '(e.g. www.YourCompany.com)'}),
                                    label='Website')

    comp_idn_phone          = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert phone number of XB company here'}),
                                    label='Phone No. (IDN)')

    comp_idn_fax            = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert fax number of XB company here'}),
                                    label='Fax No. (IDN)')

    comp_idn_email          = forms.EmailField(
                                    widget=forms.EmailInput(
                                    attrs={'placeholder': 'Please insert your XB company email address here'}),
                                    label='Email address')

    term                    = forms.ChoiceField(
                                    widget=forms.Select(
                                    attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                    choices = TERM_CHOICES,
                                    label='Term')

    term_unit               = forms.ChoiceField(
                                    widget=forms.Select(
                                    attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                    choices = TERM_UNIT_CHOICES,
                                    label='Term Unit')

    comp_idn_nationality    = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer nationality here'}),
                                    label='Nationality Representative Officer of XB Company')

    comp_idn_idnumber       = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer identity card number here'}),
                                    label='Identity Card Number Representative Officer of XB Company')

    comp_idn_rep_officer    = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer name here'}),
                                    label='Name Representative Officer of XB Company')

    contractual_agreement   = forms.FileField(
                                    widget=forms.ClearableFileInput(
                                    attrs={'type': 'file',
                                    'aria-describedby':'contractHelp'}),
                                    label='Contractual Agreement')


    class Meta:
        model = Transaction
        fields = (
            'comp_idn_name',
            'comp_idn_president',
            'comp_idn_address',
            'comp_idn_city',
            'comp_idn_province',
            'comp_idn_zip',
            'comp_idn_phone',
            'comp_idn_fax',
            'comp_idn_email',
            'comp_idn_website',
            'comp_idn_nationality',
            'comp_idn_idnumber',
            'comp_idn_rep_officer',
            'term',
            'term_unit',
            'contractual_agreement',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['comp_idn_fax'].required = False
        self.fields['comp_idn_website'].required = False
        self.fields['comp_idn_president'].required = False


class Franchise_Us_CompanyForm(forms.ModelForm):
    comp_us_name            = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company name here'}),
                                label='Name of Company')

    comp_us_president       = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert name of the person in charge of your (XA) company here'}),
                                label='Name of Company President')

    comp_us_legal_status    = forms.ChoiceField(
                                widget=forms.Select(
                                attrs={'onfocus':'this.size=4;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'},),
                                choices=LEGAL_STATUS_CHOICES,
                                label='Legal Form Status')

    comp_us_establishment   = forms.ChoiceField(
                                widget=forms.Select(
                                attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                choices=possible_years(((datetime.now()).year),1800),
                                label='Year Of establishment')

    comp_us_address         = forms.CharField(
                                widget=forms.Textarea(
                                attrs={'placeholder':'Please insert the address of your (XA) company here', 'rows':'5', 'style':'resize: none;'}),
                                label='Headquarter Address')

    comp_us_state           = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'state'}),
                                label='Headquarter state')

    comp_us_city            = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'city'}),
                                label='Headquarter city')

    comp_us_zip             = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'zip code'}),
                                label='Headquarter zip code')

    comp_us_website         = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': '(e.g. www.YourCompany.com)'}),
                                label='Website')

    comp_us_phone           = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'phone number'}),
                                label='Phone No.')

    comp_us_fax             = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'fax number'}),
                                label='Fax No.')

    comp_us_email           = forms.EmailField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company email address here',
                                'aria-describedby':'emailHint'}),
                                label='Email address')

    line_of_business        = forms.CharField(
                                widget=forms.TextInput(
                                attrs= {'placeholder': 'Please insert your (XA) company line of business here'}),
                                label='Line of Business')

    product_offering        = forms.CharField(
                                widget=forms.TextInput(
                                attrs={'placeholder': 'Please insert your (XA) company products or services offered here'}),
                                label='Product/Service Offerings')

    cert_good_standing      = forms.FileField(
                                widget=forms.ClearableFileInput(
                                attrs=  {'type': 'file',
                                'aria-describedby':'cgsHelp'}),
                                label='Upload Certificate of Good Standing')


    class Meta:
        model = Transaction
        fields =(
            'comp_us_name',
            'comp_us_president',
            'comp_us_website',
            'comp_us_legal_status',
            'comp_us_establishment',
            'comp_us_address',
            'comp_us_city',
            'comp_us_state',
            'comp_us_zip',
            'comp_us_phone',
            'comp_us_fax',
            'comp_us_email',
            'cert_good_standing',
            'line_of_business',
            'product_offering',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.help_text_inline = False
        self.fields['comp_us_fax'].required = False
        self.fields['comp_us_website'].required = False


class Franchise_Id_CompanyForm(forms.ModelForm):
    comp_idn_name           = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert XB company name here'}),
                                    label='Name of XB Company')

    comp_idn_president      = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert name of the person in charge of your (XB) company here'}),
                                    label='Name of XB Company President')

    comp_idn_address        = forms.CharField(
                                    widget=forms.Textarea(
                                    attrs={'placeholder':'Please insert the address of XB company here', 'rows':'5', 'style':'resize: none;'}),
                                    label='Address of XB Company')

    comp_idn_province       = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the Province of XB company here'}),
                                    label='Province of XB Company')

    comp_idn_city           = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the City of XB company here'}),
                                    label='City of XB Company')

    comp_idn_zip            = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert the Zip Code of XB company here'}),
                                    label='Zip Code of XB Company')

    comp_idn_website        = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': '(e.g. www.YourCompany.com)'}),
                                    label='Website')

    comp_idn_phone          = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert phone number of XB company here'}),
                                    label='Phone No. (IDN)')

    comp_idn_fax            = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert fax number of XB company here'}),
                                    label='Fax No. (IDN)')

    comp_idn_email          = forms.EmailField(
                                    widget=forms.EmailInput(
                                    attrs={'placeholder': 'Please insert your XB company email address here'}),
                                    label='Email address')

    term                    = forms.ChoiceField(
                                    widget=forms.Select(
                                    attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                    choices = TERM_CHOICES,
                                    label='Term')

    term_unit               = forms.ChoiceField(
                                    widget=forms.Select(
                                    attrs={'onfocus':'this.size=10;' , 'onblur':'this.size=1;' , 'onchange':'this.size=1; this.blur();'}),
                                    choices = TERM_UNIT_CHOICES,
                                    label='Term Unit')

    comp_idn_nationality    = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer nationality here'}),
                                    label='Nationality Representative Officer of XB Company')

    comp_idn_idnumber       = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer identity card number here'}),
                                    label='Identity Card Number Representative Officer of XB Company')

    comp_idn_rep_officer    = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Please insert your Representaive Officer name here'}),
                                    label='Name Representative Officer of XB Company')

    prospectus_agreement    = forms.FileField(
                                    widget=forms.ClearableFileInput(
                                    attrs={'type': 'file',
                                    'aria-describedby':'prospectusHelp'}),
                                    label='Prospectus Agreement')


    class Meta:
        model = Transaction
        fields = (
            'comp_idn_name',
            'comp_idn_president',
            'comp_idn_address',
            'comp_idn_city',
            'comp_idn_province',
            'comp_idn_zip',
            'comp_idn_phone',
            'comp_idn_fax',
            'comp_idn_email',
            'comp_idn_website',
            'comp_idn_nationality',
            'comp_idn_idnumber',
            'comp_idn_rep_officer',
            'term',
            'term_unit',
            'prospectus_agreement',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['comp_idn_fax'].required = False
        self.fields['comp_idn_website'].required = False
        self.fields['comp_idn_president'].required = False


class ApplicantForm(forms.ModelForm):
    applicant_name      = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Applicant Name'}),
                                    label='Name')

    applicant_position  = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'Applicant Position in US company'}),
                                    label='Position')

    applicant_city      = forms.CharField(
                                    widget=forms.TextInput(
                                    attrs={'placeholder': 'City'}),
                                    label='City')


    class Meta:
        model = Transaction
        fields = (
            'applicant_name',
            'applicant_position',
            'applicant_city',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
