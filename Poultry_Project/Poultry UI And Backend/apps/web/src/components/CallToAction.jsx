import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button.jsx';

const CallToAction = () => {
	return (
		<section className="py-24 bg-gradient-to-br from-accent to-pink-700 relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjIiIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4xIi8+PC9zdmc+')] opacity-30"></div>
      <div className="container mx-auto px-4 text-center relative z-10">
        <motion.h2 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-4xl md:text-5xl font-black text-white mb-6 drop-shadow-lg"
        >
          Ready to safeguard your flock?
        </motion.h2>
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.1 }}
          className="text-pink-100 text-xl mb-10 max-w-2xl mx-auto font-medium drop-shadow-md"
        >
          Start using our AI-powered diagnostic tool today for early detection and better poultry health management.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.2 }}
        >
          <Button asChild size="lg" className="bg-white text-accent hover:bg-gray-50 px-12 py-7 text-xl rounded-full shadow-2xl transition-all hover:scale-105 font-black border-2 border-white">
            <Link to="/predict">Start Analysis Now</Link>
          </Button>
        </motion.div>
      </div>
    </section>
	);
};

export default CallToAction;