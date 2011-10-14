import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Item {
    id: resultRealtime

    property string gline: ''
    property string gstation: ''
    property string gdirection: ''

    property string sourceUrl: ''
    property bool busy: true

    function refresh() {
        busy = true
        itip.load_departures(sourceUrl)
        console.log('refreshing')
    }

    onSourceUrlChanged: {
        refresh()
        console.log('source url changed: ' + sourceUrl)
    }

    Connections {
        target: itip

        onDeparturesLoaded: {
            busy = false
            departuresModel.clear()

            var departures = itip.get_departures()

            for (var d in departures) {
                console.log('departure: ' + departures[d])
                // XXX: destination might be wrong?!
                var row = {'line': resultRealtime.gline, 'station': resultRealtime.gstation, 'destination': gdirection, 'departure': departures[d]}
                console.log('inserting: ' + row)
                departuresModel.append(row)
            }
        }
    }

    Component {
         id: departureDelegate

         Item {
             width: parent.width
             height: 80

             BorderImage {
                 anchors.fill: parent
                 visible: mouseArea.pressed
                 source: theme.inverted ? 'image://theme/meegotouch-list-inverted-background-pressed-vertical-center': 'image://theme/meegotouch-list-background-pressed-vertical-center'
             }

             Item {
                 anchors.fill: parent
                 anchors.margins: UIConstants.DEFAULT_MARGIN

                 Row {
                     Text {
                         id: l
                         text: line // <----
                         anchors.verticalCenter: parent.verticalCenter
                         width: 70
                         font.pixelSize: UIConstants.FONT_XLARGE
                         font.bold: true
                         font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                         color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                     }

                     Column {
                         anchors.verticalCenter: parent.verticalCenter

                         Text {
                             id: s
                             text: station // <----
                             width: 75
                             font.pixelSize: UIConstants.FONT_LARGE
                             font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                             color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                         }

                         Text {
                             id: d
                             text: destination // <----
                             color: !theme.inverted ? UIConstants.COLOR_SECONDARY_FOREGROUND : UIConstants.COLOR_INVERTED_SECONDARY_FOREGROUND
                             font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                             font.pixelSize: UIConstants.FONT_LSMALL
                         }
                     }
                 }
             }

             Column {
                 anchors.right: parent.right
                 anchors.verticalCenter: parent.verticalCenter
                 Text {
                     id: dep
                     // FIXME strange int float transformation appears
                     text: departure
                     anchors.right: parent.right
                     anchors.rightMargin: UIConstants.DEFAULT_MARGIN
                     font.bold: true
                     font.pixelSize: UIConstants.FONT_XLARGE
                     font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                     color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                 }
             }

             MouseArea {
                 id: mouseArea
                 anchors.fill: parent
                 onClicked: {
                     console.debug("clicked: " + l.text)
                 }
             }
         }
     }

     ListView {
         id: list
         width: parent.width; height: parent.height

         header: Rectangle {
             width: parent.width
             height: childrenRect.height + 2*UIConstants.DEFAULT_MARGIN
             color: "lightsteelblue"

             Text {
                 anchors {
                     top: parent.top
                     left: parent.left
                     right: parent.right
                     margins: UIConstants.DEFAULT_MARGIN
                 }

                 text: 'Abfahrten Richtung ' + gdirection
                 elide: Text.ElideRight
                 font.bold: true
                 font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                 font.pixelSize: UIConstants.FONT_LSMALL
             }
         }

         model: ListModel {
             id: departuresModel
/*
            ListElement {
                line: "N60"
                station: "Schottentor"
                destination: "Maurer Hauptplatz"
                departure: 5
            }
            ListElement {
                line: "N38"
                station: "Schottentor"
                destination: "Grinzing"
                departure: 7
            }*/
         }
         delegate: departureDelegate

         visible: !resultRealtime.busy && resultRealtime.sourceUrl != ''
     }

     ScrollDecorator {
         id: scrolldecorator
         flickableItem: list
         platformStyle: ScrollDecoratorStyle {}
     }

     BusyIndicator {
         id: busyIndicator
         visible: resultRealtime.busy && resultRealtime.sourceUrl != ''
         running: visible
         platformStyle: BusyIndicatorStyle { size: 'large' }
         anchors.centerIn: parent
     }
}
