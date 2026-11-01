# HTML Fundamentals & Document Structure Notes

## 1. What is HTML?
HyperText Markup Language (HTML) is the foundational markup language used to structure and define the meaning of content on a webpage. It is not a programming language; it uses nested tags to build document skeletons.

## 2. What the `<head>` Contains
The `<head>` section contains invisible document metadata, character encoding declarations (`<meta charset="UTF-8">`), viewport scaling rules, external stylesheet references, and the browser tab title (`<title>`).

## 3. What the `<body>` Contains
The `<body>` section contains all visible content rendered by the browser, including headings, paragraphs, lists, images, navigation bars, and interactive forms.

## 4. Difference Between Headings and Paragraphs
* **Headings (`<h1>` - `<h6>`):** Define hierarchical titles and section headers that structure the document outline.
* **Paragraphs (`<p>`):** Define standard blocks of running textual content.

## 5. Utility of Semantic Elements (`<main>`, `<nav>`, `<header>`, etc.)
Semantic elements explicitly describe their purpose to browsers, screen readers, and security scanners. They improve code readability, accessibility, and make it easier for automated tools to analyze web application structures.

## 6. What Happens When You Modify HTML and Reload
When you edit an HTML file on disk and refresh your browser, the client re-reads the local file, re-parses the DOM tree, recalculates styles, and repaints the screen to reflect your latest updates in real time.
