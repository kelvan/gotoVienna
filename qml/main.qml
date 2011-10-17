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
        /*ToolIcon {
            platformIconId: "toolbar-view-menu"
            anchors.right: (parent === undefined) ? undefined : parent.right
            onClicked: (menu.status == DialogStatus.Closed) ? menu.open() : menu.close()
        }*/
        ToolIcon {
              enabled: mainPage.canRefresh
              platformIconId: enabled ? 'icon-m-toolbar-refresh' : 'icon-m-toolbar-refresh-dimmed'
              anchors.right: parent.right
              onClicked: mainPage.refresh()
        }
    }

    /*Menu {
        id: menu
        visualParent: pageStack
        MenuLayout {
            MenuItem { text: "Test"; onClicked: pageStack.push(Qt.resolvedUrl("test.qml")) }
        }
    }*/
}
