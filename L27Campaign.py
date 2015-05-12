__author__ = 'DMcHale'

import requests
import itertools
from collections import OrderedDict
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/generateCampaign', methods=['GET', 'POST'])
def generateCampaign():
    error = None
    if request.method == 'GET':
        campaign = request.args.get('campaignName', '')
        # locations = request.args.get('locations', '')
        keywords = request.args.get('keywords', '')
        headline = request.args.get('headline', '')
        descLineOne = request.args.get('descLineOne', '')
        descLineTwo = request.args.get('descLineTwo', '')
        displayUrl = request.args.get('displayUrl', '')
        destUrl = request.args.get('destUrl', '')
        zipCode = request.args.get('zipCode', '')
        zipRadius = request.args.get('zipRadius', '')
        # locations = locations.split('\n')
        keywords = keywords.split('\n')
        criterionType = 'Broad'
        geoKw = []
        adGroups = []
        zipList = []
        cityList = []

        apiKey = 'ddVKLJynw5T8wqB3RrSpTipiLlsrCr4QF0BqJaOgfIoM8ZP0rIql0PDLb5dOxhFd'

        r = requests.get('http://www.zipcodeapi.com/rest/' + apiKey + '/radius.json/' + zipCode + '/' + zipRadius + '/mi')
        responseJSON = r.json()

        for item in responseJSON['zip_codes']:
            zipList.append(item['zip_code'])
            cityList.append('+' + item['city'])

        #Sorts and removes duplicates from ZIP and City lists
        zipList = sorted(dict.fromkeys(zipList).keys())
        cityList = sorted(dict.fromkeys(cityList).keys())

        locations = cityList

        # Turn this into a flash message for results page!
        # if len(headline) > 45:
        #     print("Headline exceeds 35 characters!")
        # if len(descLineOne) > 35:
        #     print("Description Line One exceeds 35 characters!")
        # if len(descLineTwo) > 35:
        #     print("Description Line Two exceeds 35 characters!")

        for item in itertools.product(keywords, locations):
            adGroup = item[0].strip().replace('+', '').capitalize()
            keyWord = item[0].strip() + ' ' + item[1].strip()
            geoKw.append(campaign + '\t' + adGroup + '\t' + keyWord + '\t' + criterionType)
            adGroups.append(adGroup)

        createKeywordList = []
        for i in geoKw:
            createKeywordList.append(i + '\n')

        newAdGroups = list(OrderedDict.fromkeys(adGroups))

        createAdList = []
        for adGroup in newAdGroups:
            createAdList.append(campaign + '\t' + adGroup + '\t' + headline + '\t' + descLineOne + '\t' + descLineTwo + '\t'
                                   + displayUrl + '\t' + destUrl + '\n')


        campaignSettings = campaign + '\t' + 'Enabled' + '\t' + '10' + '\t' + 'Search Network Only'

        locationSettings = []
        for zip in zipList:
            locationSettings.append(campaign + '\t' + zip + '\t' + 'Postal Code')

        return render_template('results.html', campaignSettings = campaignSettings, locationSettings = locationSettings,
                               campaign = campaign, locations = locations, keywords = keywords,
                               headline = headline, descLineOne = descLineOne, descLineTwo = descLineTwo,
                               displayUrl = displayUrl, destUrl = destUrl, keywordList = createKeywordList, adList = createAdList)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
