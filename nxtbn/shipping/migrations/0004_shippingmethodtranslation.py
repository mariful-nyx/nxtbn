# Generated by Django 4.2.11 on 2025-01-05 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0003_alter_shippingrate_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingMethodTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(choices=[('en-US', 'English (United States)'), ('en-GB', 'English (United Kingdom)'), ('en-CA', 'English (Canada)'), ('en-AU', 'English (Australia)'), ('en-IN', 'English (India)'), ('en-AE', 'English (United Arab Emirates)'), ('en-SG', 'English (Singapore)'), ('en-NZ', 'English (New Zealand)'), ('en-IE', 'English (Ireland)'), ('en-ZA', 'English (South Africa)'), ('en-PH', 'English (Philippines)'), ('en-FJ', 'English (Fiji)'), ('en-IL', 'English ( Israel)'), ('he-IL', 'Hebrew ( Israel)'), ('bn-BD', 'Bangla (Bangladesh)'), ('bn-IN', 'Bangla (India)'), ('fr-FR', 'French (France)'), ('fr-CA', 'French (Canada)'), ('fr-BE', 'French (Belgium)'), ('fr-CH', 'French (Switzerland)'), ('es-ES', 'Spanish (Spain)'), ('es-MX', 'Spanish (Mexico)'), ('es-AR', 'Spanish (Argentina)'), ('es-CO', 'Spanish (Colombia)'), ('es-US', 'Spanish (United States)'), ('ar-AE', 'Arabic (United Arab Emirates)'), ('ar-SA', 'Arabic (Saudi Arabia)'), ('ar-EG', 'Arabic (Egypt)'), ('ar-MA', 'Arabic (Morocco)'), ('zh-CN', 'Chinese (Simplified, China)'), ('zh-HK', 'Chinese (Traditional, Hong Kong)'), ('zh-TW', 'Chinese (Traditional, Taiwan)'), ('hi-IN', 'Hindi (India)'), ('de-DE', 'German (Germany)'), ('de-AT', 'German (Austria)'), ('de-CH', 'German (Switzerland)'), ('pt-PT', 'Portuguese (Portugal)'), ('pt-BR', 'Portuguese (Brazil)'), ('ru-RU', 'Russian (Russia)'), ('ru-BY', 'Russian (Belarus)'), ('ru-KZ', 'Russian (Kazakhstan)'), ('ja-JP', 'Japanese (Japan)'), ('ko-KR', 'Korean (South Korea)'), ('it-IT', 'Italian (Italy)'), ('it-CH', 'Italian (Switzerland)'), ('nl-NL', 'Dutch (Netherlands)'), ('nl-BE', 'Dutch (Belgium)'), ('el-GR', 'Greek (Greece)'), ('tr-TR', 'Turkish (Turkey)'), ('sv-SE', 'Swedish (Sweden)'), ('no-NO', 'Norwegian (Norway)'), ('da-DK', 'Danish (Denmark)'), ('fi-FI', 'Finnish (Finland)'), ('pl-PL', 'Polish (Poland)'), ('vi-VN', 'Vietnamese (Vietnam)'), ('th-TH', 'Thai (Thailand)'), ('id-ID', 'Indonesian (Indonesia)'), ('ms-MY', 'Malay (Malaysia)'), ('uk-UA', 'Ukrainian (Ukraine)'), ('cs-CZ', 'Czech (Czech Republic)'), ('sk-SK', 'Slovak (Slovakia)'), ('hu-HU', 'Hungarian (Hungary)'), ('ro-RO', 'Romanian (Romania)'), ('bg-BG', 'Bulgarian (Bulgaria)'), ('hr-HR', 'Croatian (Croatia)'), ('sr-RS', 'Serbian (Serbia)'), ('sl-SI', 'Slovenian (Slovenia)'), ('lt-LT', 'Lithuanian (Lithuania)'), ('lv-LV', 'Latvian (Latvia)'), ('et-EE', 'Estonian (Estonia)'), ('mt-MT', 'Maltese (Malta)'), ('is-IS', 'Icelandic (Iceland)'), ('sq-AL', 'Albanian (Albania)'), ('mk-MK', 'Macedonian (North Macedonia)'), ('eu-ES', 'Basque (Spain)'), ('gl-ES', 'Galician (Spain)'), ('cy-GB', 'Welsh (United Kingdom)'), ('br-FR', 'Breton (France)'), ('ca-ES', 'Catalan (Spain)'), ('oc-FR', 'Occitan (France)'), ('co-FR', 'Corsican (France)'), ('gsw-DE', 'Alemannic (Germany)'), ('lb-LU', 'Luxembourgish (Luxembourg)'), ('af-ZA', 'Afrikaans (South Africa)'), ('sw-KE', 'Swahili (Kenya)'), ('rw-RW', 'Kinyarwanda (Rwanda)'), ('rn-BI', 'Kirundi (Burundi)'), ('ln-CD', 'Lingala (Congo - Kinshasa)'), ('kg-CD', 'Kongo (Congo - Kinshasa)'), ('lu-CD', 'Tshiluba (Congo - Kinshasa)'), ('ny-MW', 'Chichewa (Malawi)'), ('ny-ZM', 'Chewa (Zambia)'), ('st-LS', 'Sesotho (Lesotho)'), ('tn-BW', 'Setswana (Botswana)'), ('xog-UG', 'Soga (Uganda)'), ('ve-ZA', 'Venda (South Africa)'), ('zu-ZA', 'Zulu (South Africa)'), ('ti-ET', 'Tigrinya (Ethiopia)'), ('ps-AF', 'Pashto (Afghanistan)'), ('fa-AF', 'Dari (Afghanistan)'), ('uz-UZ', 'Uzbek (Uzbekistan)'), ('kk-KZ', 'Kazakh (Kazakhstan)'), ('tg-TJ', 'Tajik (Tajikistan)'), ('tk-TM', 'Turkmen (Turkmenistan)'), ('ky-KG', 'Kyrgyz (Kyrgyzstan)'), ('hy-AM', 'Armenian (Armenia)'), ('ka-GE', 'Georgian (Georgia)'), ('az-AZ', 'Azerbaijani (Azerbaijan)'), ('mn-MN', 'Mongolian (Mongolia)'), ('si-LK', 'Sinhala (Sri Lanka)'), ('ta-IN', 'Tamil (India)'), ('ta-LK', 'Tamil (Sri Lanka)'), ('te-IN', 'Telugu (India)'), ('kn-IN', 'Kannada (India)'), ('ml-IN', 'Malayalam (India)'), ('mr-IN', 'Marathi (India)'), ('gu-IN', 'Gujarati (India)'), ('pa-IN', 'Punjabi (India)'), ('pa-PK', 'Punjabi (Pakistan)'), ('ur-PK', 'Urdu (Pakistan)'), ('ur-IN', 'Urdu (India)'), ('ne-NP', 'Nepali (Nepal)'), ('bo-CN', 'Tibetan (China)'), ('my-MM', 'Burmese (Myanmar)'), ('km-KH', 'Khmer (Cambodia)'), ('lo-LA', 'Lao (Laos)'), ('ms-SG', 'Malay (Singapore)'), ('ms-ID', 'Malay (Indonesia)'), ('ms-BN', 'Malay (Brunei)'), ('fil-PH', 'Filipino (Philippines)'), ('mi-NZ', 'Maori (New Zealand)'), ('sm-WS', 'Samoan (Samoa)'), ('to-TO', 'Tongan (Tonga)'), ('fj-FJ', 'Fijian (Fiji)'), ('haw-US', 'Hawaiian (United States)'), ('ty-PF', 'Tahitian (French Polynesia)'), ('mg-MG', 'Malagasy (Madagascar)'), ('st-ZA', 'Sesotho (South Africa)'), ('tn-ZA', 'Tswana (South Africa)'), ('xh-ZA', 'Xhosa (South Africa)'), ('sw-TZ', 'Swahili (Tanzania)'), ('sw-UG', 'Swahili (Uganda)'), ('sw-CD', 'Swahili (Congo - Kinshasa)'), ('so-SO', 'Somali (Somalia)'), ('so-ET', 'Somali (Ethiopia)'), ('so-KE', 'Somali (Kenya)'), ('so-DJ', 'Somali (Djibouti)'), ('am-ET', 'Amharic (Ethiopia)'), ('ti-ER', 'Tigrinya (Eritrea)'), ('om-ET', 'Oromo (Ethiopia)'), ('om-KE', 'Oromo (Kenya)'), ('ha-NG', 'Hausa (Nigeria)'), ('ha-NE', 'Hausa (Niger)'), ('ha-GH', 'Hausa (Ghana)'), ('yo-NG', 'Yoruba (Nigeria)'), ('yo-BJ', 'Yoruba (Benin)'), ('ig-NG', 'Igbo (Nigeria)'), ('ff-SN', 'Fulah (Senegal)'), ('ff-GM', 'Fulah (Gambia)'), ('ff-MR', 'Fulah (Mauritania)'), ('ff-GN', 'Fulah (Guinea)'), ('wo-SN', 'Wolof (Senegal)'), ('wo-GM', 'Wolof (Gambia)'), ('wo-MR', 'Wolof (Mauritania)'), ('ber-MA', 'Berber (Morocco)'), ('ber-DZ', 'Berber (Algeria)'), ('ber-LY', 'Berber (Libya)'), ('ber-TN', 'Berber (Tunisia)'), ('ber-ML', 'Berber (Mali)'), ('ber-NG', 'Berber (Niger)')], max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('carrier', models.CharField(max_length=200)),
                ('shipping_method', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='shipping.shippingmethod')),
            ],
            options={
                'verbose_name': 'Shipping Method Translation',
                'verbose_name_plural': 'Shipping Method Translations',
                'unique_together': {('language_code', 'shipping_method')},
            },
        ),
    ]
