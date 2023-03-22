// source: chatGPT query:
// i have this on my package json 
//  "postbuild": "react-scripts build && copyfiles -u 1 'build/**/*.*' '../backend'"
// and it seems to not be working and by that i mean the build folder in the backend is not being updated by the new build folder after running npm run build from a react app

const fs = require('fs-extra');

(async () => {
    try {
        await fs.copy('./build', "../backend/build", {overwrite: true});
        console.log('copying building to backend succeeded');
    } catch (error) {
        console.error("Error copying build folder", error);
    }
})();


//"postbuild": "echo 'postbuild is running' && react-scripts build && copyfiles -u 1 'build/**/*.*' '../backend/build'"