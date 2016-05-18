#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent)
{
    setupUIParameters();
    createFileMenu();
    createToolsMenu();
    createContainer();

    euler = new Euler();
    connect(euler, SIGNAL(receivedMathString(int, int, QString)), this, SLOT(receivedMathString(int, int, QString)));

    renderer = new Renderer(minimumWidth(), minimumHeight());
    renderer->windowWidth = minimumWidth();

    // Create splitter
    QSplitter *splitter = new QSplitter;
    splitter->setOrientation(Qt::Vertical);
    container->layout()->addWidget(splitter);

    // Create tabs
    tabs = new QTabWidget(this);
    tabs->setDocumentMode(true);
    tabs->setTabsClosable(true);
    tabs->setStyleSheet("QTabWidget { left: 5px; border: none; background: #FFF; /* move to the right by 5px */ } QTabBar::tab { font: Monaco; color: white; background: #666; } QTabBar::tab:selected { background: #444 }");
    tabs->setMovable(true);
    splitter->addWidget(tabs);

    createNewTab();

    // Create workspace
    workspace = new Workspace(this);
    splitter->addWidget(workspace);
    connect(euler, SIGNAL(receivedWorkspace(int, int, QVariantMap)), workspace, SLOT(receivedWorkspace(int, int, QVariantMap)));

//     Create Command panel
    cmdpanel = new CmdPanel(this);
    container->layout()->addWidget(cmdpanel);

    // Create console
    console = new Console(this);
    splitter->addWidget(console);
    connect(euler, SIGNAL(receivedMsg(QString)), console, SLOT(receivedMsg(QString)));
    connect(euler, SIGNAL(receivedError(QString)), console, SLOT(receivedError(QString)));

}

MainWindow::~MainWindow()
{
//    delete ui;
}

void MainWindow::createToolsMenu()
{
    QMenu *toolsMenu = menuBar()->addMenu(tr("&Tools"));

    // Restart core
    QAction *coreAct = new QAction(tr("&Restart core"), this);
    coreAct->setShortcut(QKeySequence(tr("Ctrl+R")));
    connect(coreAct, SIGNAL(triggered(bool)), this, SLOT(on_actionRestart_core_triggered()));
    toolsMenu->addAction(coreAct);

    // Clear console
    QAction *clearConsoleAct = new QAction(tr("&Clear console"), this);
    clearConsoleAct->setShortcut(QKeySequence(tr("Ctrl+Shift+K")));
    connect(clearConsoleAct, SIGNAL(triggered(bool)), this, SLOT(on_actionClear_console_triggered()));
    toolsMenu->addAction(clearConsoleAct);

    // Zoom
    QAction *zoom100 = new QAction(tr("&Zoom 100%"), this);
    zoom100->setShortcut(QKeySequence(tr("Ctrl+1")));
    connect(zoom100, SIGNAL(triggered(bool)), this, SLOT(on_action100_triggered()));
    toolsMenu->addAction(zoom100);

    QAction *zoom150 = new QAction(tr("&Zoom 150%"), this);
    zoom150->setShortcut(QKeySequence(tr("Ctrl+2")));
    connect(zoom150, SIGNAL(triggered(bool)), this, SLOT(on_action150_triggered()));
    toolsMenu->addAction(zoom150);

    QAction *zoom200 = new QAction(tr("&Zoom 200%"), this);
    zoom200->setShortcut(QKeySequence(tr("Ctrl+3")));
    connect(zoom200, SIGNAL(triggered(bool)), this, SLOT(on_action200_triggered()));
    toolsMenu->addAction(zoom200);
}

void MainWindow::setupUIParameters()
{
    QGuiApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    setMinimumSize(ptX(600), ptY(600));

    pal = palette();

//    Dark theme
//    pal.setColor(QPalette::Base, QColor("#333"));
//    pal.setColor(QPalette::Background, QColor("#333"));
//    pal.setColor(QPalette::Text, QColor("#FFF"));

    pal.setColor(QPalette::Base, QColor("#FFF"));
    pal.setColor(QPalette::Background, QColor("#FFF"));
    pal.setColor(QPalette::Text, QColor("#000"));

    setPalette(pal);

    setFont(QFont("Monaco", 12));
}

void MainWindow::createContainer()
{
    container = new QWidget(this);
    container->setLayout(new QVBoxLayout());
    container->layout()->setMargin(0);
    setCentralWidget(container);
}

void MainWindow::createFileMenu()
{
    QMenu *fileMenu = menuBar()->addMenu(tr("&File"));

    // Open menu
    QAction *newAct = new QAction(tr("&New"), this);
    newAct->setShortcut(QKeySequence(tr("Ctrl+N")));
    connect(newAct, SIGNAL(triggered(bool)), this, SLOT(on_actionNew_triggered()));
    fileMenu->addAction(newAct);


    // Open menu
    QAction *openAct = new QAction(tr("&Open"), this);
    openAct->setShortcut(QKeySequence(tr("Ctrl+O")));
    connect(openAct, SIGNAL(triggered(bool)), this, SLOT(on_actionOpen_triggered()));
    fileMenu->addAction(openAct);

    // Save menu
    QAction *saveAct = new QAction(tr("&Save"), this);
    saveAct->setShortcut(QKeySequence(tr("Ctrl+S")));
    connect(saveAct, SIGNAL(triggered(bool)), this, SLOT(on_actionSave_triggered()));
    fileMenu->addAction(saveAct);

    // Export menu
    QAction *exportAct = new QAction(tr("&Export"), this);
    exportAct->setShortcut(QKeySequence(tr("Ctrl+E")));
    connect(exportAct, SIGNAL(triggered(bool)), this, SLOT(on_actionExport_triggered()));
    fileMenu->addAction(exportAct);

    // Close menu
    QAction *closeAct = new QAction(tr("Close file"), this);
    closeAct->setShortcut(QKeySequence(tr("Ctrl+W")));
    connect(closeAct, SIGNAL(triggered(bool)), this, SLOT(on_actionClose_triggered()));
    fileMenu->addAction(closeAct);
}

void MainWindow::initRenderer() {
    renderer->move(this->pos());
}

void MainWindow::closeEvent(QCloseEvent *e) {
    if (isWindowModified()) {
        QMessageBox msgBox;
        msgBox.setText("The document has been modified.");
        msgBox.setInformativeText("Do you want to save your changes?");
        msgBox.setStandardButtons(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
        msgBox.setDefaultButton(QMessageBox::Save);
        int ret = msgBox.exec();
        if (ret == QMessageBox::Save) saveFile();
        else if (ret == QMessageBox::Cancel) e->ignore();
        else if (ret == QMessageBox::Discard) {
            setWindowModified(false);
        }
    } else {
        euler->terminate();
        renderer->close();
        qDebug() << "Terminate python.";
    }
}

void MainWindow::moveEvent(QMoveEvent *)
{
    renderer->move(pos());
}

void MainWindow::scrollTo(Paragraph *paragraph)
{
    ((QScrollArea*) tabs->currentWidget())->ensureWidgetVisible(paragraph, 0, 600);
}

// Tabs

void MainWindow::createNewTab(bool empty, QString fileName)
{
    QFrame *contents = new QFrame(this);
    QVBoxLayout *layout = new QVBoxLayout;
    layout->setContentsMargins(ptY(10), ptY(10), ptY(10), ptY(256));
    layout->setAlignment(Qt::AlignTop);
    contents->setLayout(layout);
    contents->setPalette(pal);
    contents->setFocusPolicy(Qt::NoFocus);

    QScrollArea *scrollArea = new QScrollArea(this);
    scrollArea->setWidget(contents);
    scrollArea->setWidgetResizable(true);
    scrollArea->setFocusPolicy(Qt::NoFocus);
//    scrollArea->setSizeAdjustPolicy(QAbstractScrollArea::AdjustToContents);
    scrollArea->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    contents->show();

    tabs->addTab(scrollArea, fileName);
    tabs->setCurrentWidget(scrollArea);
    connect(tabs, SIGNAL(tabBarClicked(int)), this, SLOT(onTabChange(int)));
    setWindowTitle("iEuler - " + fileName);

    paragraphID = 0;
    if (!empty) addNewParagraph();
}


Paragraph * MainWindow::addNewParagraph(int lineNumber, QString mathString)
{
    int tabIndex = tabs->currentIndex();
    int index = paragraphID;
    Paragraph *paragraph = new Paragraph(this,
                                         euler,
                                         renderer,
                                         tabIndex,
                                         index,
                                         mathString);

    if (lineNumber < 0) {
        getTabContents()->layout()->addWidget(paragraph);
    } else {
        ((QVBoxLayout*) getTabContents()->layout())->insertWidget(lineNumber, paragraph);
    }

    connect(paragraph, SIGNAL(keyboardAction(int, Paragraph*)), this, SLOT(keyboardAction(int, Paragraph*)));
    connect(this, SIGNAL(lineNumberChanged(int, QLayout*)), paragraph, SLOT(lineNumberChanged(int, QLayout*)));

    emit lineNumberChanged(tabIndex, getTabContents()->layout());

    paragraphID++;

    paragraph->focus();

    qApp->processEvents();
    scrollTo(paragraph);
    return paragraph;
}

void MainWindow::keyboardAction(int action, Paragraph *target)
{
    int lineNumber = getTabContents()->layout()->indexOf(target);
    int count = getTabContents()->layout()->count();
    if (action == MathEdit::EVAL_AND_CONTINUE) {
        if (lineNumber == count - 1) {
            if (!target->isEmpty()) addNewParagraph();
        } else {
            focusNextChild();
        }
    } else if (action == MathEdit::DELETE_LINE) {
        if (count > 1) {
            if (lineNumber == 0) {
                focusNextChild();
            } else {
                focusPreviousChild();
            }
            getTabContents()->layout()->removeWidget(target);
            emit lineNumberChanged(tabs->currentIndex(), getTabContents()->layout());
            delete target;
        }
    } else if (action == MathEdit::MOVE_UP) {
        if (lineNumber > 0) {
            focusPreviousChild();
            scrollTo(target);
        }
    } else if (action == MathEdit::MOVE_DOWN) {
        if (lineNumber < count - 1) {
            focusNextChild();
            scrollTo(target);
        }
    } else if (action == MathEdit::INSERT_ABOVE) {
        Paragraph *paragraph = addNewParagraph(lineNumber);

        int index = getTabContents()->layout()->indexOf(paragraph);

        if (index > 0) {
            Paragraph *before = (Paragraph *) getTabContents()->layout()->itemAt(index - 1)->widget();
            setTabOrder(before->mathEdit, paragraph->mathEdit);
        }

        setTabOrder(paragraph->mathEdit, target->mathEdit);

    } else if (action == MathEdit::INSERT_BELOW) {
        Paragraph *paragraph = addNewParagraph(lineNumber + 1);

        int index = getTabContents()->layout()->indexOf(paragraph);

        setTabOrder(target->mathEdit, paragraph->mathEdit);

        if (index < count - 1) {
            Paragraph *after = (Paragraph *) getTabContents()->layout()->itemAt(index + 1)->widget();
            setTabOrder(paragraph->mathEdit, after->mathEdit);
        }
    } else if (action == MathEdit::DUPLICATE_LINE) {
        Paragraph *paragraph = addNewParagraph(lineNumber + 1, target->mathString);

        int index = getTabContents()->layout()->indexOf(paragraph);

        setTabOrder(target->mathEdit, paragraph->mathEdit);

        if (index < count - 1) {
            Paragraph *after = (Paragraph *) getTabContents()->layout()->itemAt(index + 1)->widget();
            setTabOrder(paragraph->mathEdit, after->mathEdit);
        }
    }
}

// File I/O

void MainWindow::openFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getOpenFileName(this,
                   tr("Open iEuler file"), dir, tr("iEuler files (*.eulerc)"));
    if (path != "") {
        QFileInfo fi(path);
        createNewTab(true, fi.baseName());

        euler->sendOpenFileRequest(path);
    }

}

void MainWindow::saveFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
                   tr("Save iEuler file"), dir, tr("Text Files (*.euler)"));

    if (path != "") {
        QFileInfo fi(path);
        euler->sendSaveFileRequest(path);
        tabs->setTabText(tabs->currentIndex(), fi.baseName());
        setWindowTitle("iEuler - " + fi.baseName());
    }
}

void MainWindow::exportFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
                   tr("Export PDF file"), dir, tr("PDF Files (*.pdf)"));

    if (path != "") {
        euler->sendExportRequest(path);
    }
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

void MainWindow::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_Escape) {
        cmdpanel->hide();
    }
}

void MainWindow::receivedMathString(int, int, QString mathString)
{
    addNewParagraph(-1, mathString);
}

void MainWindow::on_action100_triggered()
{
    renderer->setZoomFactor(100);
}

void MainWindow::on_action150_triggered()
{
    renderer->setZoomFactor(150);
}

void MainWindow::on_action200_triggered()
{
    renderer->setZoomFactor(200);
}

void MainWindow::on_actionNew_triggered()
{
    createNewTab();
}

void MainWindow::on_actionClose_triggered()
{
    if (tabs->currentIndex() > 0) {
        tabs->setCurrentIndex(tabs->currentIndex() - 1);
        tabs->removeTab(tabs->currentIndex() + 1);
    }
}

QWidget* MainWindow::getTabContents() {
    return ((QScrollArea*) tabs->currentWidget())->widget();
}

void MainWindow::on_actionOpen_triggered()
{
    openFile();
}

void MainWindow::on_actionSave_triggered()
{
    saveFile();
}

void MainWindow::on_actionExport_triggered()
{
    exportFile();
}

void MainWindow::onTabChange(int index)
{
    setWindowTitle("iEuler - " + tabs->tabText(index));
}

void MainWindow::on_actionRestart_core_triggered()
{
    euler->restartCore();
    renderer->restart();
}

void MainWindow::on_actionClear_console_triggered()
{
    console->clear();
}
