#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDebug>
#include <QTabWidget>
#include <QScrollArea>
#include <QFileDialog>
#include <QFileInfo>
#include <QStandardPaths>
#include <QMessageBox>
#include <QSplitter>
#include <QMenuBar>
//#include <QtWebEngineWidgets>
//#include <QWebEngineView>
#include <QMoveEvent>
#include <QThread>

#include "cmdpanel.h"
#include "paragraph.h"
#include "euler.h"
#include "util.h"
#include "console.h"
#include "workspace.h"
#include "mathedit.h"
#include "lasemrender.h"

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
//    Renderer *renderer;
    LASEMRender *lsm_render;
    QPalette pal;
    Console *console;
    Workspace *workspace;

    int paragraphID;

    void createFileMenu();
    void createToolsMenu();

    void setupUIParameters();
    void createContainer();

    Paragraph *addNewParagraph(int targetIndex = -1, QString mathString = "");
    void createNewTab(bool empty = false, QString fileName = "Untitled");

    void openFile();
    void saveFile();
    void exportFile();

    QWidget *getTabContents();

    void closeEvent(QCloseEvent *event);
    void moveEvent(QMoveEvent *);

    void scrollTo(Paragraph *paragraph);

protected:
    void keyPressEvent(QKeyEvent *);

signals:
    void outputReady(int lineIndex, QString latexString);
    void lineNumberChanged(int tabIndex, QLayout *mainLayout);

private slots:
    void receivedMathString(int, int, QString mathString);
    void keyboardAction(int action, Paragraph *target);

    void on_actionShow_command_panel_triggered();
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
    void on_actionClear_console_triggered();
};

#endif // MAINWINDOW_H
