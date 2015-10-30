#-------------------------------------------------
#
# Project created by QtCreator 2015-09-23T13:11:33
#
#-------------------------------------------------

QT       += core gui
QT       += webkit
QT       += webkitwidgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = mathnotesgui
TEMPLATE = app


SOURCES += \
    codeinput.cpp \
    main.cpp \
    mainwindow.cpp \
    group.cpp \
    cmdpanel.cpp \
    plotview3d.cpp \
    mathrenderer.cpp \
    euler.cpp \
    renderer.cpp \
    mathwidget.cpp \
    paragraph.cpp \
    mathedit.cpp

HEADERS  += \
    codeinput.h \
    mainwindow.h \
    group.h \
    cmdpanel.h \
    plotview3d.h \
    mathrenderer.h \
    euler.h \
    renderer.h \
    mathwidget.h \
    paragraph.h \
    mathedit.h

FORMS    += \
    mainwindow.ui

RESOURCES += \
    math_resources.qrc
