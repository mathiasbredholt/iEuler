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
#include <QDebug>
#include "mathrenderer.h"
#include <QTabWidget>
#include <QScrollArea>
#include <QFileDialog>
#include <QFileInfo>
#include <QStandardPaths>
#include <QMessageBox>
#include <QStringList>
#include "paragraph.h"
#include "euler.h"


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
    QTabWidget *tabs;
    CmdPanel *cmdpanel;
    QProcess *proc;
    Euler *euler;
    Renderer *renderer;

    int numberOfLines;

    void createGroup(QString cmd = "");
    void addNewParagraph(QString mathString = "");
    void createNewTab(bool empty = false, QString fileName = "Untitled.euler");
    void initSubprocess();
    void initRenderer();

    void openFile();
    void saveFile();
    void exportFile();

    QWidget *getTabContents();

    void closeEvent(QCloseEvent *event);

    bool loadingMode;


protected:
    void keyPressEvent(QKeyEvent *);

signals:
    void outputReady(int lineIndex, QString latexString);

private slots:
    void receivedMathString(int index, QString mathString);

    void readStandardOutput();
    void readStandardError();
    void previewCode(CodeInput *target, QString inputString);
    void evaluateCode(CodeInput *target, QString inputString);
    void newLine_triggered(int index);
    void deleteGroup(QWidget* target);
    void on_actionShow_command_panel_triggered();
    void changeFocus_triggered(bool up, int index);
    void on_action100_triggered();
    void on_action150_triggered();
    void on_action200_triggered();
    void on_actionNew_triggered();
    void on_actionClose_triggered();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();
    void on_actionExport_triggered();
    void onTabChange(int index);
};

#endif // MAINWINDOW_H
