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
#include <QObject>
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

    int numberOfLines;

    void createNewCodeLine();
    void initSubprocess();

protected:
    void keyPressEvent(QKeyEvent *);

signals:
    void outputReady(int lineIndex, QString latexString);

private slots:
    void readStandardOutput();
    void readStandardError();
    void previewCode(CodeInput *target, QString inputString);
    void evaluateCode(CodeInput *target, QString inputString);
    void deleteGroup(QWidget* target);
    void on_actionShow_command_panel_triggered();
    void arrowsPressed(bool upArrowPressed);
    void on_action100_triggered();
    void on_action150_triggered();
    void on_action200_triggered();
};

#endif // MAINWINDOW_H
