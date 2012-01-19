import QtQuick 1.1
import com.nokia.meego 1.0

Dialog {
   id: updateDialog
   property alias text: messageContent.text

   content:Item {
     id: message
     height: 85
     width: parent.width
     Text {
       id: messageContent
       font.pixelSize: 22
       anchors.centerIn: parent
       color: "white"
       text: "If you see this message\nsend me an email\nto <gotovienna@logic.at>\ndescribe what you're doing getting this message"
     }
   }

   buttons: ButtonRow {
     style: ButtonStyle { }
       anchors.horizontalCenter: parent.horizontalCenter
       Button {text: "OK"; onClicked: updateDialog.accept()}
     }
   }
