
import QtQuick 1.0

Rectangle {
    id: aboutBox
    property string appName: 'MyApp x.y.z'
    property string websiteURL: 'http://example.org/'
    property string copyright: ''
    property string license: ''
    property string iconFilename: ''
    width: 480
    height: 800

    function show() { opacity = 1 }

    color: '#dd000000'
    opacity: 0
    Behavior on opacity { PropertyAnimation { } }

    MouseArea {
        anchors.fill: parent
        onClicked: aboutBox.opacity = 0
    }

    Column {
        anchors.centerIn: parent
        spacing: 5
        scale: Math.pow(parent.opacity, 3)
        width: 440

        Item {
            height: aboutBoxIcon.sourceSize.height
            width: parent.width

            Image {
                id: aboutBoxIcon
                anchors.centerIn: parent
                source: aboutBox.iconFilename
            }
        }

        Text {
            color: 'white'
            font.pixelSize: 30
            font.bold: true
            text: aboutBox.appName
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            color: 'white'
            text: aboutBox.websiteURL
            font.pixelSize: 25
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            color: 'white'
            font.pixelSize: 17
            text: '\n' + aboutBox.copyright + '\n' + aboutBox.license
            anchors.horizontalCenter: parent.horizontalCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }
}

