// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const BASE_URL =  "http://127.0.0.1:5000";



// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "hacksmith" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('hacksmith.documenting', async function () {
		const editor = vscode.window.activeTextEditor;
		if (editor) {
			const selection = editor.selection;
			const selectedText = editor.document.getText(selection);
	
			// Fetch request using `selectedText` as the `code` parameter
			try {
				 
				const response = await fetch(`${BASE_URL}/single`, {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ content: selectedText, type: "code" }) // Adjust type as needed
				});
	
				const data = await response.json();
				const generatedText = data.content; // Extract and format the generated code
	
				// Replace the selected text with the formatted generated result
				await editor.edit(editBuilder => {
					editBuilder.replace(selection, generatedText);
				});
			
			
				vscode.window.showInformationMessage(`Generated Result: ${JSON.stringify(data)}`);
			} catch (error) {
				console.log(error);
				vscode.window.showErrorMessage(`Error: ${error.message}`);
			}
		}
	});
	
	context.subscriptions.push(disposable);
	
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
