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
#include "cmdpanel.h"

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
    CmdPanel *cmdpanel;
    QProcess *proc;

    void createNewCodeLine();
    void initSubprocess();

signals:
    void outputReady();

private slots:
    void readStandardOutput();
    void evaluateCode(CodeInput *target, QString inputString);
    void deleteGroup(Group* target);
    void on_actionShow_command_panel_triggered();
};

#endif // MAINWINDOW_H
