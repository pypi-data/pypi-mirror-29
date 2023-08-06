

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n != 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "All": "Alle",
    "An error has occurred.": "Ein Fehler ist aufgetreten.",
    "An error of type {code} occurred.": "Ein Fehler ist aufgetreten. Fehlercode: {code}",
    "Barcode area": "QR-Code-Bereich",
    "Cart expired": "Warenkorb abgelaufen",
    "Close message": "Schlie\u00dfen",
    "Comment:": "Kommentar:",
    "Contacting Stripe \u2026": "Kontaktiere Stripe \u2026",
    "Copied!": "Kopiert!",
    "Count": "Anzahl",
    "Do you really want to leave the editor without saving your changes?": "M\u00f6chten Sie den Editor wirklich schlie\u00dfen ohne Ihre \u00c4nderungen zu speichern?",
    "Error while uploading your PDF file, please try again.": "Es gab ein Problem beim Hochladen der PDF-Datei, bitte erneut versuchen.",
    "Generating messages \u2026": "Generiere Nachrichten\u2026",
    "Group of objects": "Gruppe von Objekten",
    "Marked as paid": "Als bezahlt markiert",
    "None": "Keine",
    "Object": "Objekt",
    "Others": "Sonstige",
    "Paid orders": "Bezahlte Bestellungen",
    "Placed orders": "Get\u00e4tigte Bestellungen",
    "Press Ctrl-C to copy!": "Dr\u00fccken Sie Strg+C zum Kopieren!",
    "QR Code": "QR-Code",
    "Saving failed.": "Speichern fehlgeschlagen.",
    "Text object": "Text-Objekt",
    "The PDF background file could not be loaded for the following reason:": "Die Hintergrund-PDF-Datei konnte nicht geladen werden:",
    "The items in your cart are no longer reserved for you.": "Die Produkte in Ihrem Warenkorb sind nicht mehr f\u00fcr Sie reserviert.",
    "The items in your cart are reserved for you for one minute.": [
      "Die Produkte in Ihrem Warenkorb sind noch eine Minute f\u00fcr Sie reserviert.",
      "Die Produkte in Ihrem Warenkorb sind noch {num} Minuten f\u00fcr Sie reserviert."
    ],
    "The request took to long. Please try again.": "Diese Anfrage hat zu lange gedauert. Bitte erneut versuchen.",
    "Ticket design": "Ticket-Design",
    "Total revenue": "Gesamtumsatz",
    "Unknown error.": "Unbekannter Fehler.",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "Ihre Anfrage wird an den Server gesendet. Wenn dies l\u00e4nger als eine Minute dauert, pr\u00fcfen Sie bitte Ihre Internetverbindung. Danach k\u00f6nnen Sie diese Seite neu laden und es erneut versuchen.",
    "We are processing your request \u2026": "Wir verarbeiten Ihre Anfrage \u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "Wir k\u00f6nnen den Server aktuell nicht erreichen, versuchen es aber weiter. Letzter Fehlercode: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "Wir k\u00f6nnen den Server aktuell nicht erreichen. Bitte versuchen Sie es noch einmal. Fehlercode: {code}",
    "Your request has been queued on the server and will now be processed. Depending on the size of your event, this might take up to a few minutes.": "Ihre Anfrage ist auf dem Server angekommen und wird nun verarbeitet. Je nach Gr\u00f6\u00dfe der Veranstaltung kann dies einige Minuten dauern.",
    "Your request has been queued on the server and will now be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "Ihre Anfrage ist auf dem Server angekommen und wird nun verarbeitet. Wenn dies l\u00e4nger als zwei Minuten dauert, kontaktieren Sie uns bitte oder gehen Sie in Ihrem Browser einen Schritt zur\u00fcck und versuchen es erneut.",
    "widget\u0004Buy": "In den Warenkorb",
    "widget\u0004Close": "Schlie\u00dfen",
    "widget\u0004Close ticket shop": "Ticket-Shop schlie\u00dfen",
    "widget\u0004Continue": "Weiter",
    "widget\u0004FREE": "GRATIS",
    "widget\u0004Only available with a voucher": "Nur mit Gutschein verf\u00fcgbar",
    "widget\u0004Redeem": "Einl\u00f6sen",
    "widget\u0004Redeem a voucher": "Gutschein einl\u00f6sen",
    "widget\u0004Reserved": "Reserviert",
    "widget\u0004See variations": "Varianten zeigen",
    "widget\u0004Sold out": "Ausverkauft",
    "widget\u0004The cart could not be created. Please try again later": "Der Warenkorb konnte nicht erstellt werden. Bitte erneut versuchen.",
    "widget\u0004The ticket shop could not be loaded.": "Der Ticket-Shop konnte nicht geladen werden.",
    "widget\u0004Voucher code": "Gutscheincode",
    "widget\u0004Waiting list": "Warteliste",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart. Click on this message to continue checkout with your cart.": "Sie haben einen aktiven Warenkorb f\u00fcr diese Veranstaltung. Wenn Sie mehr Produkte ausw\u00e4hlen, werden diese zu Ihrem Warenkorb hinzugef\u00fcgt. Klicken Sie auf diese Meldung um den Kauf des bestehenden Warenkorbs fortzusetzen oder den Warenkorb zu ver\u00e4ndern.",
    "widget\u0004currently available: %s": "aktuell verf\u00fcgbar: %s",
    "widget\u0004from %(currency)s %(price)s": "ab %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "inkl. %(rate)s% %(taxname)s",
    "widget\u0004minimum amount to order: %s": "minimale Bestellmenge: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "zzgl. %(rate)s% %(taxname)s",
    "widget\u0004ticketing powered by <a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">pretix</a>": "ticketing powered by <a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">pretix</a>"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j. F Y H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d.%m.%Y %H:%M:%S",
      "%d.%m.%Y %H:%M:%S.%f",
      "%d.%m.%Y %H:%M",
      "%d.%m.%Y",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j. F Y",
    "DATE_INPUT_FORMATS": [
      "%d.%m.%Y",
      "%d.%m.%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": "1",
    "MONTH_DAY_FORMAT": "j. F",
    "NUMBER_GROUPING": "3",
    "SHORT_DATETIME_FORMAT": "d.m.Y H:i",
    "SHORT_DATE_FORMAT": "d.m.Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

