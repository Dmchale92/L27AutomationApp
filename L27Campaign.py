__author__ = 'DMcHale'
import os
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
        locations = request.args.get('locations', '')
        keywords = request.args.get('keywords', '')
        headline = request.args.get('headline', '')
        descLineOne = request.args.get('descLineOne', '')
        descLineTwo = request.args.get('descLineTwo', '')
        displayUrl = request.args.get('displayUrl', '')
        destUrl = request.args.get('destUrl', '')
        locations = locations.split('\n')
        keywords = keywords.split('\n')
        criterionType = 'Broad'
        geoKw = []
        adGroups = []
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

        for location in createKeywordList:
            print location
        for keyword in createAdList:
            print keyword

        return render_template('results.html', campaign = campaign, locations = locations, keywords = keywords,
                               headline = headline, descLineOne = descLineOne, descLineTwo = descLineTwo,
                               displayUrl = displayUrl, destUrl = destUrl, keywordList = createKeywordList, adList = createAdList)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
