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
    property bool isStation: false

    function refresh() {
        busy = true
        console.debug('refreshing')

        if (isStation) {
            console.debug('station based')
            itip.load_station_departures(gstation)
        } else {
            console.debug('one line')
            itip.load_departures(sourceUrl)
        }
    }

    function isCorrectInput () {
        return resultRealtime.sourceUrl != '' || (resultRealtime.isStation && resultRealtime.gstation != '')
    }

    onGstationChanged: {
        console.debug('gstation changed')
        refresh()
    }

    Connections {
        target: itip

        onDeparturesLoaded: {
            busy = false
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
                    spacing: 10
                    Text {
                        id: l
                        text: model.line // <----
                        anchors.verticalCenter: parent.verticalCenter
                        //width: 70
                        font.pixelSize: UIConstants.FONT_XLARGE
                        font.bold: true
                        font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                        color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                    }

                    Column {
                        anchors.verticalCenter: parent.verticalCenter

                        Text {
                            id: s
                            text: model.station // <----
                            width: parent.parent.parent.width - l.width - dep.width - 15
                            elide: Text.ElideRight
                            font.pixelSize: UIConstants.FONT_LARGE
                            font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                            color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                        }

                        Text {
                            id: d
                            text: model.direction // <---   -
                            width: parent.parent.parent.width - l.width - dep.width - 15
                            elide: Text.ElideRight
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
                    text: model.time
                    anchors.right: parent.right
                    anchors.rightMargin: UIConstants.DEFAULT_MARGIN
                    font.italic: lowfloor
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
            radius: 5.0
            smooth: true

            Text {
                id: header

                anchors {
                    top: parent.top
                    left: parent.left
                    right: parent.right
                    margins: UIConstants.DEFAULT_MARGIN
                }

                text: 'Richtung ' + gdirection
                elide: Text.ElideRight
                font.bold: true
                font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                font.pixelSize: UIConstants.FONT_LSMALL
            }
        }

        model: resultModel
        delegate: departureDelegate

        visible: !resultRealtime.busy && isCorrectInput()
    }

    ScrollDecorator {
        id: scrolldecorator
        flickableItem: list
        platformStyle: ScrollDecoratorStyle {}
    }

    BusyIndicator {
        id: busyIndicator
        visible: resultRealtime.busy && isCorrectInput()
        running: visible
        platformStyle: BusyIndicatorStyle { size: 'large' }
        anchors.centerIn: parent
    }
}
