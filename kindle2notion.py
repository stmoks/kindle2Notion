from notion.client import NotionClient
from notion.collection import NotionDate
from notion.block import QuoteBlock, TextBlock, PageBlock

from datetime import datetime
import string
import os
import unicodedata
from settings import CLIPPINGS_FILE, NOTION_TOKEN, NOTION_TABLE_ID

# create the Kindle Clippings class and the accompanying attribute/methods


class KindleClippings(object):
    # seems conventional to define the class as KindleClippings(object) even though the var is only passed in the init method

    # important to note the difference between class object attributes (are the same regardless of the instance) vs instance attributes that differ from instance to instance

    def __init__(self, clippingsFile):
        self.clippings = self.getAllClippings(clippingsFile)

    def getAllClippings(self, clippingsFile):
        allClippings = open(clippingsFile, 'r', encoding="utf-8-sig").read()
        allClippings = unicodedata.normalize("NFKD", allClippings)
        return self.parseClippings(allClippings)

    def parseClippings(self, allClippings):
        allClippings = allClippings.split("==========")
        total = len(allClippings)
        print("Found", total, "notes and highlights")
        counter = 1
        clipCollection = []
        for eachClipping in allClippings:
            eachClipping = eachClipping.strip().split("\n")

            # Sometimes a null text or a bookmark is selected in the clipping. In these cases, we need to check the length of the cell.
            if len(eachClipping) >= 3:
                firstLine = eachClipping[0]
                # Second line after = marks, used to identify the type
                secondLine = eachClipping[1]

                print("Processing note/highlight number",
                      counter, "/", total, "from", firstLine)

                # TODO: Author name might be stated as follows: "Voltaire (francois Marie Arouet)". So author name should be extracted with Regex.
                title_author = eachClipping[0].replace(
                    '(', '|').replace(')', '')

                # Converted author datatype from string to array for all type of notes. If author is single it'll be converted to string without comma
                title, *author = title_author.split('|')
                title = title.strip()

                # Please regard this hack. This operation can return some pairs like (page and date), (location and date)
                # or 3 values: (page, location, date)
                # We'll get last item for date.
                # Parameter Explanation
                # 1. pageAndloc: page and location of the highlight
                # 2. optLocAndDate: Optionally Location can return and date can return or only date can return as array
                pageAndloc, *optLocAndDate = secondLine.strip().split('|')

                addedOn = optLocAndDate[-1]
                dateAdded = datetime.strptime(
                    addedOn, ' Added on %A, %d %B %Y %X')
                clipping = eachClipping[3]

                lastClip = {
                    'Title': title,
                    'Author': ",".join(author),
                    'Page': None,
                    'Location': None,
                    'Date Added': dateAdded,
                    'Clipping': clipping
                }

                # TODO: These conditions can also be collapsed. New logic can check "Your X at/on location/page" and change it dynamically
                if '- Your Highlight at location ' in secondLine:
                    location = pageAndloc.replace(
                        '- Your Highlight at location ', '').replace(' ', '')
                    lastClip["Location"] = location

                elif '- Your Note on location ' in secondLine:
                    location = pageAndloc.replace(
                        '- Your Note on location ', '').replace(' ', '')
                    lastClip["Location"] = location

                elif '- Your Highlight on page ' in secondLine and 'location ' in secondLine:
                    page = pageAndloc.replace(
                        '- Your Highlight on page ', '').replace(' ', '')
                    location = optLocAndDate[0].replace(
                        ' location ', '').replace(' ', '')
                    lastClip["Page"] = page
                    lastClip["Location"] = location

                elif '- Your Note on page ' in secondLine and 'location ' in secondLine:
                    page = pageAndloc.replace(
                        '- Your Note on page ', '').replace(' ', '')
                    location = optLocAndDate[0].replace(
                        ' location ', '').replace(' ', '')
                    lastClip["Page"] = page
                    lastClip["Location"] = location

                elif '- Your Highlight on page ' in secondLine and 'location ' not in secondLine:
                    page = pageAndloc.replace(
                        '- Your Highlight on page ', '').replace(' ', '')
                    lastClip["Page"] = page

                elif '- Your Note on page ' in secondLine and 'location ' not in secondLine:
                    page = pageAndloc.replace(
                        '- Your Note on page ', '').replace(' ', '')
                    lastClip["Page"] = page
                    # TODO: Check this.
                    print(self.getClipping())

                clipCollection.append(lastClip)
                self.addToNotion(lastClip)
                counter += 1

            else:
                # TODO: Bookmarks can also be added to the service??
                print("Skipping bookmark number:",
                      counter, "because it's empty.")
                counter += 1

        return clipCollection

    def getClipping(self):
        for i in self.clippings:
            yield i

    def lenClippings(self):
        return len(self.clippings)

    def addNewClippingToRow(self, lastClip, row, titleExists):
        clipExists = False
        if not titleExists:
            row.title = lastClip['Title']
            row.author = lastClip['Author']
            row.highlights = 0
        parentPage = client.get_block(row.id)
        allClippings = parentPage.children.filter(QuoteBlock)
        for eachClip in allClippings:
            if lastClip['Clipping'].strip() == eachClip.title:
                clipExists = True
        if clipExists == False:
            if lastClip['Location'] != None:
                if lastClip['Page'] != None:
                    parentPage.children.add_new(
                        TextBlock,
                        title="Page: " + lastClip['Page'] + "\tLocation: " + lastClip['Location'] + "\tDate Added: " + str(
                            lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                    )
                else:
                    parentPage.children.add_new(
                        TextBlock,
                        title="Location: " + lastClip['Location'] + "\tDate Added: " + str(
                            lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                    )
            else:
                parentPage.children.add_new(
                    TextBlock,
                    title="Page: " + lastClip['Page'] + "\tDate Added: " + str(
                        lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                )
            parentPage.children.add_new(
                QuoteBlock,
                title=lastClip['Clipping']
            )
            row.highlights += 1
            row.last_highlighted = NotionDate(lastClip['Date Added'])
            row.last_synced = NotionDate(datetime.now())

    def addToNotion(self, lastClip):
        titleExists = False
        clipExists = False
        global cv
        allRows = cv.collection.get_rows()
        if allRows != []:
            for eachRow in allRows:
                if lastClip['Title'] == eachRow.title:
                    titleExists = True
                    row = eachRow
        if not titleExists:
            row = cv.collection.add_row()
            row.title = lastClip['Title']
            row.author = lastClip['Author']
            row.highlights = 0
        parentPage = client.get_block(row.id)
        allClippings = parentPage.children.filter(QuoteBlock)
        for eachClip in allClippings:
            if lastClip['Clipping'].strip() == eachClip.title:
                clipExists = True
        if clipExists == False:
            if lastClip['Location'] != None:
                if lastClip['Page'] != None:
                    parentPage.children.add_new(
                        TextBlock,
                        title="Page: " + lastClip['Page'] + "\tLocation: " + lastClip['Location'] + "\tDate Added: " + str(
                            lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                    )
                else:
                    parentPage.children.add_new(
                        TextBlock,
                        title="Location: " + lastClip['Location'] + "\tDate Added: " + str(
                            lastClip['Date Added'].strftime("%A, %d %B %Y %I:%M:%S %p"))
                    )
            else:
                parentPage.children.add_new(
                    TextBlock,
                    title="Page: " + "\tDate Added: " +
                    str(lastClip['Date Added'].strftime(
                        "%A, %d %B %Y %I:%M:%S %p"))
                )
            parentPage.children.add_new(
                QuoteBlock,
                title=lastClip['Clipping']
            )
            row.highlights += 1
            row.last_highlighted = NotionDate(lastClip['Date Added'])
            row.last_synced = NotionDate(datetime.now())

#--------------------------------------------------------------------------------#


client = NotionClient(token_v2=NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
allRows = cv.collection.get_rows()
print(cv.parent.views)

ch = KindleClippings(CLIPPINGS_FILE)
