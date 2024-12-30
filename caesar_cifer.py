import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class EnhancedCaesarCipherGUI extends JFrame implements ActionListener {
    // English letter frequency (approximate)
    private static final double[] ENGLISH_FREQ = {
        8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094,
        6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929,
        0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150,
        1.974, 0.074
    };

    // GUI components
    private JTextField messageField, shiftField;
    private JTextArea resultArea;
    private JButton encryptButton, decryptButton, bruteForceButton, freqAnalysisButton;

    public EnhancedCaesarCipherGUI() {
        setTitle("Enhanced Caesar Cipher Program");
        setSize(600, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(8, 1));

        panel.add(new JLabel("Enter your message:"));
        messageField = new JTextField();
        panel.add(messageField);

        panel.add(new JLabel("Enter shift value (leave empty for cracking):"));
        shiftField = new JTextField();
        panel.add(shiftField);

        encryptButton = new JButton("Encrypt");
        decryptButton = new JButton("Decrypt");
        bruteForceButton = new JButton("Brute-force Crack");
        freqAnalysisButton = new JButton("Frequency Analysis Crack");

        panel.add(encryptButton);
        panel.add(decryptButton);
        panel.add(bruteForceButton);
        panel.add(freqAnalysisButton);

        resultArea = new JTextArea();
        resultArea.setEditable(false);
        panel.add(new JScrollPane(resultArea));

        add(panel);

        encryptButton.addActionListener(this);
        decryptButton.addActionListener(this);
        bruteForceButton.addActionListener(this);
        freqAnalysisButton.addActionListener(this);
    }

    public static String encrypt(String plainText, int shift) {
        StringBuilder cipherText = new StringBuilder();
        for (char letter : plainText.toCharArray()) {
            if (Character.isLetter(letter)) {
                char base = Character.isLowerCase(letter) ? 'a' : 'A';
                char encryptedLetter = (char) ((letter - base + shift + 26) % 26 + base);
                cipherText.append(encryptedLetter);
            } else if (Character.isDigit(letter)) {
                char encryptedDigit = (char) ((letter - '0' + shift + 10) % 10 + '0');
                cipherText.append(encryptedDigit);
            } else {
                cipherText.append(letter);
            }
        }
        return cipherText.toString();
    }

    public static String decrypt(String cipherText, int shift) {
        return encrypt(cipherText, -shift);
    }

    public static int findShiftByFrequency(String cipherText) {
        int probableShift = 0;
        double minChiSquared = Double.MAX_VALUE;

        for (int shift = 0; shift < 26; shift++) {
            double chiSquared = calculateChiSquared(cipherText, shift);
            if (chiSquared < minChiSquared) {
                minChiSquared = chiSquared;
                probableShift = shift;
            }
        }
        return probableShift;
    }

    private static double calculateChiSquared(String text, int shift) {
        int[] letterCount = new int[26];
        int totalLetters = 0;

        for (char c : text.toCharArray()) {
            if (Character.isLetter(c)) {
                c = Character.toLowerCase(c);
                letterCount[(c - 'a' - shift + 26) % 26]++;
                totalLetters++;
            }
        }

        double chiSquared = 0.0;
        for (int i = 0; i < 26; i++) {
            double expected = totalLetters * ENGLISH_FREQ[i] / 100;
            double observed = letterCount[i];
            chiSquared += Math.pow(observed - expected, 2) / expected;
        }

        return chiSquared;
    }

    public static String crackCipherBruteForce(String cipherText) {
        StringBuilder result = new StringBuilder("Brute-force results:\n");
        for (int shift = 1; shift < 26; shift++) {
            String possibleText = decrypt(cipherText, shift);
            result.append("Shift ").append(shift).append(": ").append(possibleText).append("\n");
        }
        return result.toString();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String message = messageField.getText();
        int shift = 0;
        String result = "";

        try {
            if (!shiftField.getText().isEmpty()) {
                shift = Integer.parseInt(shiftField.getText()) % 36;
            }

            if (e.getSource() == encryptButton) {
                result = "Encrypted message: " + encrypt(message, shift);
            } else if (e.getSource() == decryptButton) {
                result = "Decrypted message: " + decrypt(message, shift);
            } else if (e.getSource() == bruteForceButton) {
                result = crackCipherBruteForce(message);
            } else if (e.getSource() == freqAnalysisButton) {
                int predictedShift = findShiftByFrequency(message);
                result = "Predicted Shift: " + predictedShift + "\nCracked Message: " + decrypt(message, predictedShift);
            }
        } catch (Exception ex) {
            result = "Error: " + ex.getMessage();
        }

        resultArea.setText(result);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            EnhancedCaesarCipherGUI gui = new EnhancedCaesarCipherGUI();
            gui.setVisible(true);
        });
    }
}
