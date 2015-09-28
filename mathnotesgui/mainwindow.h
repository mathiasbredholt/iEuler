#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "ui_mainwindow.h"
#include "codeinput.h"
#include "group.h"
#include <QSizePolicy>
#include <QProcess>
#include<QtCore/QFile>
#include<QtCore/QTextStream>
#include <QProcess>
#include <QThread>
#include <QLabel>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

    void createNewCodeLine();

signals:
    void outputReady();

private slots:
    void evaluateCode(CodeInput *target, QString inputString);
    void deleteGroup(Group* target);
};

#endif // MAINWINDOW_H
