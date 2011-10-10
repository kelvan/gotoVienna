import QtQuick 1.1
import com.nokia.meego 1.0

PageStackWindow {
    id: appWindow

    initialPage: mainPage

    MainPage {
        id: mainPage
    }

    ToolBarLayout {
        id: commonTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (menu.status == DialogStatus.Closed) ? menu.open() : menu.close()
        }
        ToolIcon {
              enabled: appWindow.pageStack.depth > 1
              platformIconId: enabled ? "icon-m-toolbar-back" : "icon-m-toolbar-back-dimmed"
              anchors.left: parent.left
              onClicked: pageStack.pop()
             }
    }

    Menu {
        id: menu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: qsTr("Sample menu item") }
            MenuItem { text: "Test"; onClicked: pageStack.push(Qt.resolvedUrl("test.qml")) }
        }
    }
}
