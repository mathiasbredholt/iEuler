#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
//#include "ui_mainwindow.h"
#include <QDebug>
#include <QTabWidget>
#include <QScrollArea>
#include <QFileDialog>
#include <QFileInfo>
#include <QStandardPaths>
#include <QMessageBox>
#include <QtWebEngineWidgets>
#include <QWebEngineView>
#include <QMoveEvent>
#include <QThread>

#include "cmdpanel.h"
#include "paragraph.h"
#include "euler.h"
#include "util.h"
#include "console.h"
#include "workspace.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void initRenderer();

private:
//    Ui::MainWindow *ui;
    QWidget *container;
    QTabWidget *tabs;
    CmdPanel *cmdpanel;
    Euler *euler;
    Renderer *renderer;
    QPalette pal;
    Console *console;
    Workspace *workspace;

    int numberOfLines;

    void createFileMenu();
    void createToolsMenu();

    void setupUIParameters();
    void createContainer();

    void addNewParagraph(QString mathString = "");
    void createNewTab(bool empty = false, QString fileName = "Untitled");

    void openFile();
    void saveFile();
    void exportFile();

    QWidget *getTabContents();

    void closeEvent(QCloseEvent *event);
    void moveEvent(QMoveEvent *event);

    void scrollTo(Paragraph *paragraph);

protected:
    void keyPressEvent(QKeyEvent *);

signals:
    void outputReady(int lineIndex, QString latexString);

private slots:
    void receivedMathString(int tabIndex, int index, QString mathString);

    void newLine_triggered(int index);
    void deleteLine_triggered(Paragraph *target);

    void on_actionShow_command_panel_triggered();
    void changeFocus_triggered(Paragraph *paragraph, bool goUp);
    void on_action100_triggered();
    void on_action150_triggered();
    void on_action200_triggered();
    void on_actionNew_triggered();
    void on_actionClose_triggered();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();
    void on_actionExport_triggered();
    void onTabChange(int index);
    void on_actionRestart_core_triggered();
};

#endif // MAINWINDOW_H
