import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0
import "UIConstants.js" as UIConstants
import "ExtrasConstants.js" as ExtrasConstants

Page {
    tools: commonTools

    property string gline : ""
    property string gstation : ""
    property bool busy : true

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

    Component {
             id: heading
             Rectangle {
                 width: parent.width
                 height: childrenRect.height + 2*UIConstants.DEFAULT_MARGIN
                 color: "lightsteelblue"

                 Text {
                     anchors {
                         top: parent.top
                         left: parent.left
                         margins: UIConstants.DEFAULT_MARGIN
                     }

                     text: gstation + " [" + gline + "]"
                     font.bold: true
                     font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                     font.pixelSize: UIConstants.FONT_LSMALL
                 }
             }
         }

     ListView {
         id: list
         width: parent.width; height: parent.height

         header: heading

         model: ListModel {
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
            }
            ListElement {
                line: "N25"
                station: "Schottentor"
                destination: "Großfeldsiedlung"
                departure: 8
            }
            ListElement {
                line: "N41"
                station: "Schottentor"
                destination: "Pötzleinsdorf"
                departure: 12
            }
            ListElement {
                line: "N43"
                station: "Schottentor"
                destination: "Neuwaldegg"
                departure: 12
            }
            ListElement {
                line: "N66"
                station: "Schottentor"
                destination: "Liesing S"
                departure: 20
            }
            ListElement {
                line: "N38"
                station: "Schottentor"
                destination: "Grinzing"
                departure: 22
            }
            ListElement {
                line: "N25"
                station: "Schottentor"
                destination: "Großfeldsiedlung"
                departure: 35
            }
            ListElement {
                line: "N60"
                station: "Schottentor"
                destination: "Maurer Hauptplatz"
                departure: 35
            }
            ListElement {
                line: "N38"
                station: "Schottentor"
                destination: "Grinzing"
                departure: 37
            }
            ListElement {
                line: "N41"
                station: "Schottentor"
                destination: "Pötzleinsdorf"
                departure: "03:12"
            }
            ListElement {
                line: "N43"
                station: "Schottentor"
                destination: "Neuwaldegg"
                departure: 42
            }
            ListElement {
                line: "N66"
                station: "Schottentor"
                destination: "Liesing S"
                departure: 50
            }
            ListElement {
                line: "N38"
                station: "Schottentor"
                destination: "Grinzing"
                departure: 52
            }
         }
         delegate: departureDelegate
     }

     ScrollDecorator {
         id: scrolldecorator
         flickableItem: list
         platformStyle: ScrollDecoratorStyle {}
     }

     BusyIndicator {
         id: busyIndicator
         visible: busy
         running: true
         platformStyle: BusyIndicatorStyle { size: 'large' }
         anchors.centerIn: parent
     }
}
