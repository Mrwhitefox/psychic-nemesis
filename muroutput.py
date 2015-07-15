# -*- coding: utf-8 -*-
import datetime
import pygal
import os
from html import escape     


def rawEcho(table):
    for row in table:
        for col in row:
            print(col, end="\t")
        print(" ")



def export_stackedBars(data, title, filename):
    values = list(data[0])
    xLabels = list(data[1])
    valuesTags = list(data[2])
    today = datetime.date.today()

    stackedbar_chart = pygal.HorizontalStackedBar(label_font_size=8, legend_at_bottom=True)
    stackedbar_chart.title = title + today.strftime(' (%Y/%m/%d)')
    stackedbar_chart.x_labels = xLabels
    
    for tag, value in zip(valuesTags, values):
        stackedbar_chart.add(tag, value)

    saveChart(stackedbar_chart, filename)

def export_lines(data, title, filename):
    values = list(data[0])
    xLabels = list(data[1])
    valuesTags = list(data[2])
    today = datetime.date.today()   

    chart = pygal.Line( x_label_rotation=90, legend_at_bottom=True)
    chart.title = title + today.strftime(' (%Y/%m/%d)')
    chart.x_labels = xLabels

    for tag, value in zip(valuesTags, values):
        chart.add(tag, value)
    saveChart(chart, filename)


def export_map(data, title, filename):
    worldmap_chart = pygal.Worldmap(legend_at_bottom=True)
    worldmap_chart.title = title
    for row in data:
      worldmap_chart.add(row[0], row[1])
    saveChart(worldmap_chart, filename)

def export_pyramid(data, title, filename):
    values = list(data[0])
    xLabels = list(data[1])
    valuesTags = list(data[2])

    chart = pygal.Pyramid(human_readable=True, legend_at_bottom=True)
    chart.title = title
    chart.x_labels = xLabels
    for tag, value in zip(valuesTags, values):
        chart.add(tag, value)
    saveChart(chart, filename)


def export_html(data, title, filename):
    title = data[0]
    headers = data[1]
    rows = data[2]
    nbCol = len(headers)



    
    html =  "<html><head><title>{0}</title>  </head><body bgcolor='lightgrey'> <h1>{0}</h1><table>".format(title)

    html += "<tr bgcolor='#5F5'>"    
    for head in headers:
        html += "<td>{0}</td>".format(head)
    html += "</tr>"

    for row in rows:
        html += "<tr>"
        for col in row:
            html += "<td>{0}</td>".format(accentsToHml(str(col)) if col is not None else "&nbsp; ")
        html += "</tr>\n"
    html += "</table></body></html>"
    saveText(str(html), filename)

def saveChart(chart, filename):
    filePath = os.path.join("output", "{0}.svg".format(filename).replace("/", os.sep).replace(":", "-"))
    os.remove(filePath) if os.path.exists(filePath) else None
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    chart.render_to_file(filePath)


def saveText(text, filename):
    filePath = os.path.join("output", "{0}.htm".format(filename).replace("/", os.sep).replace(":", "-"))
    os.remove(filePath) if os.path.exists(filePath) else None
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    f = open(filePath,'w', encoding="utf-8")
    f.write(text)
    f.close()


def accentsToHml(text):
    htmlcodes = ['&Aacute;', '&aacute;', '&Agrave;', '&Acirc;', '&agrave;', '&Acirc;', '&acirc;', '&Auml;', '&auml;', '&Atilde;', '&atilde;', '&Aring;', '&aring;', '&Aelig;', '&aelig;', '&Ccedil;', '&ccedil;', '&Eth;', '&eth;', '&Eacute;', '&eacute;', '&Egrave;', '&egrave;', '&Ecirc;', '&ecirc;', '&Euml;', '&euml;', '&Iacute;', '&iacute;', '&Igrave;', '&igrave;', '&Icirc;', '&icirc;', '&Iuml;', '&iuml;', '&Ntilde;', '&ntilde;', '&Oacute;', '&oacute;', '&Ograve;', '&ograve;', '&Ocirc;', '&ocirc;', '&Ouml;', '&ouml;', '&Otilde;', '&otilde;', '&Oslash;', '&oslash;', '&szlig;', '&Thorn;', '&thorn;', '&Uacute;', '&uacute;', '&Ugrave;', '&ugrave;', '&Ucirc;', '&ucirc;', '&Uuml;', '&uuml;', '&Yacute;', '&yacute;', '&yuml;', '&copy;', '&reg;', '&trade;', '&euro;', '&cent;', '&pound;', '&lsquo;', '&rsquo;', '&ldquo;', '&rdquo;', '&laquo;', '&raquo;', '&mdash;', '&ndash;', '&deg;', '&plusmn;', '&frac14;', '&frac12;', '&frac34;', '&times;', '&divide;', '&alpha;', '&beta;', '&infin']
    funnychars = ['\xc1','\xe1','\xc0','\xc2','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3','\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9','\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc','\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2','\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf','\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc','\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018','\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc','\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e']
    newtext = ""
    for char in text:
        if char not in funnychars:
            newtext = newtext + char
        else:
            newtext  = newtext + htmlcodes[funnychars.index(char)]
    return(newtext)