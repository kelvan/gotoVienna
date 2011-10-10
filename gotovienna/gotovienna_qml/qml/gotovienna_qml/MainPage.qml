import QtQuick 1.1
import com.nokia.meego 1.0

Page {
    tools: commonTools

    TextField {
        placeholderText: 'origin'

        id: origin
        text: "Test"
        anchors {
            top: parent.top
            left: parent.left
            topMargin: 20
            leftMargin: 10
            rightMargin: 10
        }
        width: parent.width - 20
    }

    TextField {
        placeholderText: 'destination'
        id: destination
        anchors {
            top: origin.bottom
            left: parent.left
            right: parent.right
            topMargin: 10
            leftMargin: 10
            rightMargin: 10
        }
    }

    Button {
        id: btnSearch
        text: 'Search'
        anchors {
            top: destination.bottom
            topMargin: 10
            horizontalCenter: parent.horizontalCenter
        }
    }

    ListModel {
            id: delegateModel
            ListElement {
                item_index: 0
                item_name: "Item 1";
                item_description: "Description 1";

            }
            ListElement {
                item_index: 1
                item_name: "Item 2"
                item_description: "Description 2"
            }
            ListElement {
                item_index: 2
                item_name: "Item 3"
                item_description: "Description 3"
            }
        }

    Component {
            id: departureDelegate
            Item {
                visible: false
                id: wrapper
                width: parent.width
                height: 40
                Column {
                    x: 5; y: 5
                    Text { text: '<b>Name:</b>' + item_name }
                    Text { text: '<b>Description:</b>' + item_description }
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: departureList.currentIndex = item_index
                }
            }
        }

    Component {
        id: departureHilight
        Rectangle {
            visible: false
            width: parent.width
            height: 70
            color: "lightsteelblue"
            radius: 5
        }
    }

    PinchArea {
        anchors {
            top: btnSearch.bottom
            topMargin: 20
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        pinch.maximumScale: 3
        pinch.minimumScale: 1

        onPinchUpdated: {
            console.debug(pinch.scale)
        }

        function swap(o, d) {
            var tmp = d.text
            d.text = o.text
            o.text = tmp
        }
        onPinchFinished: swap(origin, destination)
    }

    ListView {
        id: departureList
        anchors {
            top: btnSearch.bottom
            topMargin: 20
            left: parent.left
            leftMargin: 20
            right: parent.right
            rightMargin: 20
        }
        width: parent.width
        model: delegateModel
        delegate: departureDelegate
        highlight: departureHilight
        focus: false
    }
}
