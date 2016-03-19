/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.6.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionShow_command_panel;
    QAction *action100;
    QAction *action150;
    QAction *action200;
    QAction *actionNew;
    QAction *actionClose;
    QAction *actionSave;
    QAction *actionOpen;
    QAction *actionExport;
    QAction *actionRestart_core;
    QWidget *container;
    QHBoxLayout *horizontalLayout;
    QMenuBar *menuBar;
    QMenu *menuTools;
    QMenu *menuZoom;
    QMenu *menuFile;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->setWindowModality(Qt::NonModal);
        MainWindow->resize(800, 600);
        MainWindow->setDocumentMode(false);
        actionShow_command_panel = new QAction(MainWindow);
        actionShow_command_panel->setObjectName(QStringLiteral("actionShow_command_panel"));
        actionShow_command_panel->setCheckable(false);
        action100 = new QAction(MainWindow);
        action100->setObjectName(QStringLiteral("action100"));
        action150 = new QAction(MainWindow);
        action150->setObjectName(QStringLiteral("action150"));
        action200 = new QAction(MainWindow);
        action200->setObjectName(QStringLiteral("action200"));
        actionNew = new QAction(MainWindow);
        actionNew->setObjectName(QStringLiteral("actionNew"));
        actionClose = new QAction(MainWindow);
        actionClose->setObjectName(QStringLiteral("actionClose"));
        actionSave = new QAction(MainWindow);
        actionSave->setObjectName(QStringLiteral("actionSave"));
        actionOpen = new QAction(MainWindow);
        actionOpen->setObjectName(QStringLiteral("actionOpen"));
        actionExport = new QAction(MainWindow);
        actionExport->setObjectName(QStringLiteral("actionExport"));
        actionRestart_core = new QAction(MainWindow);
        actionRestart_core->setObjectName(QStringLiteral("actionRestart_core"));
        container = new QWidget(MainWindow);
        container->setObjectName(QStringLiteral("container"));
        horizontalLayout = new QHBoxLayout(container);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        horizontalLayout->setContentsMargins(0, 0, 0, 0);
        MainWindow->setCentralWidget(container);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 800, 31));
        menuTools = new QMenu(menuBar);
        menuTools->setObjectName(QStringLiteral("menuTools"));
        menuZoom = new QMenu(menuBar);
        menuZoom->setObjectName(QStringLiteral("menuZoom"));
        menuFile = new QMenu(menuBar);
        menuFile->setObjectName(QStringLiteral("menuFile"));
        MainWindow->setMenuBar(menuBar);

        menuBar->addAction(menuFile->menuAction());
        menuBar->addAction(menuTools->menuAction());
        menuBar->addAction(menuZoom->menuAction());
        menuTools->addAction(actionShow_command_panel);
        menuTools->addAction(actionRestart_core);
        menuZoom->addAction(action100);
        menuZoom->addAction(action150);
        menuZoom->addAction(action200);
        menuFile->addAction(actionNew);
        menuFile->addAction(actionOpen);
        menuFile->addAction(actionSave);
        menuFile->addAction(actionExport);
        menuFile->addAction(actionClose);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "iEuler", 0));
        actionShow_command_panel->setText(QApplication::translate("MainWindow", "Show command panel", 0));
        actionShow_command_panel->setShortcut(QApplication::translate("MainWindow", "Ctrl+Shift+P", 0));
        action100->setText(QApplication::translate("MainWindow", "100%", 0));
        action100->setShortcut(QApplication::translate("MainWindow", "Ctrl+0", 0));
        action150->setText(QApplication::translate("MainWindow", "150%", 0));
        action150->setShortcut(QApplication::translate("MainWindow", "Ctrl+1", 0));
        action200->setText(QApplication::translate("MainWindow", "200%", 0));
        action200->setShortcut(QApplication::translate("MainWindow", "Ctrl+2", 0));
        actionNew->setText(QApplication::translate("MainWindow", "New", 0));
        actionNew->setShortcut(QApplication::translate("MainWindow", "Ctrl+N", 0));
        actionClose->setText(QApplication::translate("MainWindow", "Close tab", 0));
        actionClose->setShortcut(QApplication::translate("MainWindow", "Ctrl+W", 0));
        actionSave->setText(QApplication::translate("MainWindow", "Save", 0));
        actionSave->setShortcut(QApplication::translate("MainWindow", "Ctrl+S", 0));
        actionOpen->setText(QApplication::translate("MainWindow", "Open", 0));
        actionOpen->setShortcut(QApplication::translate("MainWindow", "Ctrl+O", 0));
        actionExport->setText(QApplication::translate("MainWindow", "Export", 0));
        actionExport->setShortcut(QApplication::translate("MainWindow", "Ctrl+E", 0));
        actionRestart_core->setText(QApplication::translate("MainWindow", "Restart core", 0));
        actionRestart_core->setShortcut(QApplication::translate("MainWindow", "Ctrl+R", 0));
        menuTools->setTitle(QApplication::translate("MainWindow", "Tools", 0));
        menuZoom->setTitle(QApplication::translate("MainWindow", "Zoom", 0));
        menuFile->setTitle(QApplication::translate("MainWindow", "File", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
