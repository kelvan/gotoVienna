
import Qt 4.7

Rectangle {
    width: 800
    height: 400
    color: 'black'

    property alias model: lv.model


    ListView {
        id: lv
        anchors.fill: parent

        delegate: OverviewItem {
            onShowDetails: lv.showDetails(details)
        }

        states: [
            State {
                name: 'overview'
            },
            State {
                name: 'details'
                PropertyChanges {
                    target: detailsRect
                    opacity: 1
                    scale: 1
                }
            }
        ]

        Rectangle {
            id: detailsRect
            width: parent.width - 50
            height: parent.height - 50
            anchors.centerIn: parent
            scale: 0
            opacity: 0
            color: '#aaa'

            border {
                color: '#888'
                width: 10
            }

            Behavior on opacity { PropertyAnimation { duration: 250 }}

            Behavior on scale {
                PropertyAnimation {
                    duration: 500
                    easing.type: Easing.InCubic
                }
            }

            Text {
                id: detailsTitle

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                horizontalAlignment: Text.AlignHCenter
                anchors.topMargin: 20
                font.pixelSize: 30
            }
            
            Text {
                id: detailsList

                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: detailsTitle.bottom
                horizontalAlignment: Text.AlignLeft
                font.pixelSize: 20
            }

            MouseArea {
                anchors.fill: parent
                onClicked: lv.state = 'overview'
            }
        }

        function showDetails(details) {
            detailsTitle.text = 'Details for ' + details.time_from + '-' + details.time_to
            detailsList.text = ''
            for(var k=0; k < details.details.length; k++) {
            	if (details.details[k].station != '') {
            		detailsList.text += 'Station: ' + details.details[k].station + '\n' + details.details[k].info + '\n'
            	}
            }
            lv.state = 'details'
        }
    }
}

