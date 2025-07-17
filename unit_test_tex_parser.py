import unittest
from tex_parser_strip import extract_chunks

class TestTexParser(unittest.TestCase):

    def test_extract_chunks_basic(self):
        sample_tex = r"""
        \section{Introduction}
        This is an intro paragraph.
        \begin{align*}
        E = mc^2 \label{eq:einstein} \\
        \end{align*}

        \section{Cooling Function}
        The cooling rate is defined as:
        \begin{align*}
        \Lambda(T) &= n_e n_H \Lambda_T \cite{smith2020} \\
        \end{align*}
        It depends on temperature.
        """

        chunks = extract_chunks(sample_tex)
        self.assertEqual(len(chunks), 5)

        # First section text
        self.assertEqual(chunks[0]['section'], 'Introduction')
        self.assertIn("intro paragraph", chunks[0]['text'])

        # First section equation (cleaned)
        self.assertEqual(chunks[1]['equation'].strip().rstrip('\\').strip(), "E = mc^2")

        # Second section text before equation
        self.assertEqual(chunks[2]['section'], 'Cooling Function')
        self.assertIn("cooling rate is defined", chunks[2]['text'])

        # Text after equation
        self.assertIn("temperature", chunks[4]['text'])

if __name__ == "__main__":
    unittest.main()
