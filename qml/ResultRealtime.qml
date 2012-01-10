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
        console.log('refreshing')

        if (isStation) {
            console.log('station based')
            itip.load_station_departures(gstation)
        } else {
            console.log('one line')
            itip.load_departures(sourceUrl)
        }
    }

    function isCorrectInput () {
        return resultRealtime.sourceUrl != '' || (resultRealtime.isStation && resultRealtime.gstation != '')
    }

    onGstationChanged: {
        refresh()
    }

    Connections {
        target: itip

        onDeparturesLoaded: {
            busy = false
            departuresModel.clear()

            var departures = itip.get_departures()

            for (var d in departures) {
                console.log('time: ' + departures[d].time)
                var row = {'line': departures[d].line, 'station': departures[d].station, 'destination': departures[d].direction, 'departure': departures[d].time, 'lowfloor': departures[d].lowfloor}
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
                    spacing: 10
                    Text {
                        id: l
                        text: line // <----
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
                            text: station // <----
                            width: parent.parent.parent.width - l.width - dep.width - 15
                            elide: Text.ElideRight
                            font.pixelSize: UIConstants.FONT_LARGE
                            font.family: ExtrasConstants.FONT_FAMILY_LIGHT
                            color: !theme.inverted ? UIConstants.COLOR_FOREGROUND : UIConstants.COLOR_INVERTED_FOREGROUND
                        }

                        Text {
                            id: d
                            text: destination // <----
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
                    text: departure
                    anchors.right: parent.right
                    anchors.rightMargin: UIConstants.DEFAULT_MARGIN
                    font.italic: lowfloor == 1
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

        model: ListModel {
            id: departuresModel
        }
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
