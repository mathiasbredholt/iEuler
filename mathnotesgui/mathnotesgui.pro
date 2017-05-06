#-------------------------------------------------
#
# Project created by QtCreator 2015-09-23T13:11:33
#
#-------------------------------------------------

QT       += core gui
QT       += network
QT       += widgets
#QT       += webchannel
#QT       += webenginewidgets

TARGET = mathnotesgui
TEMPLATE = app


SOURCES += \
    main.cpp \
    mainwindow.cpp \
    cmdpanel.cpp \
    plotview3d.cpp \
    euler.cpp \
    renderer.cpp \
    mathwidget.cpp \
    paragraph.cpp \
    mathedit.cpp \
    cmdpanelitem.cpp \
    util.cpp \
    console.cpp \
    workspace.cpp \
    lasemrender.cpp

HEADERS  += \
    mainwindow.h \
    cmdpanel.h \
    plotview3d.h \
    euler.h \
    renderer.h \
    mathwidget.h \
    paragraph.h \
    mathedit.h \
    cmdpanelitem.h \
    util.h \
    console.h \
    workspace.h \
    lasemrender.h

FORMS    +=

RESOURCES += \
    katex.qrc

DISTFILES +=
