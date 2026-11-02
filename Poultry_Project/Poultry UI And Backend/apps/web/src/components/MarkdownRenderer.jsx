import React from 'react';
import ReactMarkdown from 'react-markdown';

const MarkdownRenderer = ({ markdown }) => {
  if (!markdown) return null;

  return (
    <div className="prose prose-sm sm:prose-base dark:prose-invert max-w-none text-gray-200">
      <ReactMarkdown
        components={{
          h3: ({ node, ...props }) => (
            <h3 className="text-xl font-bold text-white mt-6 mb-3" {...props} />
          ),
          strong: ({ node, ...props }) => (
            <strong className="font-bold text-white" {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul className="list-disc ml-6 my-4 space-y-2" {...props} />
          ),
          li: ({ node, ...props }) => (
            <li className="text-gray-200" {...props} />
          ),
          p: ({ node, ...props }) => (
            <p className="my-3 leading-relaxed" {...props} />
          ),
        }}
      >
        {markdown}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;